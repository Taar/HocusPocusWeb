import sys
import transaction
import argparse

from sqlalchemy.orm.exc import NoResultFound
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
from getpass import getpass


def main(settings):

    dbmaker = get_dbmaker(get_engine(settings))
    dbsession = get_session(transaction.manager, dbmaker)

    users = get_users(dbsession)

    if not users:
        print("No users in the database")
        sys.exit(1)

    lines = ''
    for user in users:
        lines += parse_hostapd_lines(user)

    populate_file(settings['hostapd'], lines)

    if not validate_files_contents(settings['hostapd'], lines):
        print("Failed to place users into {}".format(settings['hostapd']))
        sys.exit(1)

    dnsmasq_lines = ''
    for user in users:
        dnsmasq_lines += parse_dnsmasq_lines(user)

    with open(settings['dnsmasq'], 'r') as f:
        data = f.read()
        config, _ = data.split('# USER-START')

    data = config.strip()
    data += "\n# USER-START\n"
    data += dnsmasq_lines
    populate_file(settings['dnsmasq'], data)

    if not validate_files_contents(settings['dnsmasq'], data):
        print("Failed to place users into {}".format(settings['dnsmasq']))
        sys.exit(1)

    print("Complete!")


def populate_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def validate_files_contents(path, data):
    with open(path, 'r') as f:
        content = f.read()
        return content == data


def parse_hostapd_lines(user):
    template = "# {name}\n{mac_address}\n"
    return template.format(name=user.name, mac_address=user.mac_address)


def parse_dnsmasq_lines(user):
    template = "# {name}\ndhcp-host={mac_address},{ip_address}\n"
    return template.format(name=user.name,
                           mac_address=user.mac_address,
                           ip_address=user.ip_address)


def get_users(dbsession):
    return dbsession.query(User).all()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add user to database')
    parser.add_argument('config_uri', help='Pyramid config file')

    args = parser.parse_args()
    setup_logging(args.config_uri)
    settings = get_appsettings(args.config_uri)

    main(settings)
