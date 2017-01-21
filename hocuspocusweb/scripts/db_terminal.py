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
from ptpython.repl import embed


def main(settings):

    dbmaker = get_dbmaker(get_engine(settings))
    dbsession = get_session(transaction.manager, dbmaker)

    embed(globals(), locals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add user to database')
    parser.add_argument('config_uri', help='Pyramid config file')

    args = parser.parse_args()
    setup_logging(args.config_uri)
    settings = get_appsettings(args.config_uri)

    main(settings)
