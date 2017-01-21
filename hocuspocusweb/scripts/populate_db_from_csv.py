import sys
import transaction
import argparse
import csv
import string

from sqlalchemy.exc import DBAPIError

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )
from hocuspocusweb.models.meta import (
    get_session,
    get_engine,
    get_dbmaker,
    )
from hocuspocusweb.models import User
from random import choice
from collections import namedtuple


UserPassword = namedtuple("UserPassword", "name email password")


def main(settings, csv_path):

    dbmaker = get_dbmaker(get_engine(settings))
    dbsession = get_session(transaction.manager, dbmaker)

    users_password_pairs = []
    # If there are any errors all the changes will be rolled back
    # FIX: getting a segmentation fault on rollback. Need to look into why this
    # is happening :(
    with transaction.manager:
        empty_user_table(dbsession)
        with open(csv_path, 'r') as csv_file:
            for user in csv.DictReader(csv_file):
                user.update({'password': generate_password()})
                dbsession.add(User(**user))
                users_password_pairs.append(
                    UserPassword(user['name'], user['email'], user['password'])
                )

    template = "{name} [{email}] {password}"
    for pair in users_password_pairs:
        print(
            template.format(
                name=pair.name,
                email=pair.email,
                password=pair.password
            )
        )

    print("Completed successfully!")
    sys.exit(0)


def generate_password(length=9):
    chars = string.ascii_uppercase + string.digits
    return "".join([choice(chars) for x in range(0, length)])


def empty_user_table(dbsession):
    return dbsession.query(User).delete()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add user to database')
    parser.add_argument('config_uri', help='Pyramid config file')
    parser.add_argument('csv', help='CSV with user data')

    args = parser.parse_args()
    setup_logging(args.config_uri)
    settings = get_appsettings(args.config_uri)

    main(settings, args.csv)
