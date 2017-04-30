import pytest
import transaction
import logging

from pyramid import testing


class DataBase():

    def __init__(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('hocuspocusweb.models.meta')
        settings = self.config.get_settings()

        from hocuspocusweb.models.meta import (
            get_session,
            get_engine,
            get_dbmaker,
            )

        self.engine = get_engine(settings)
        dbmaker = get_dbmaker(self.engine)

        self.session = get_session(transaction.manager, dbmaker)

    def init_database(self):
        from hocuspocusweb.models.meta import Base
        Base.metadata.create_all(self.engine)

    def rollback(self):
        from hocuspocusweb.models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.create_all(self.engine)


@pytest.fixture(scope='module')
def db():
    return DataBase()


@pytest.fixture(scope='module')
def log():
    return logging.getLogger('tests')
