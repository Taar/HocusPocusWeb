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

        self.tm = transaction.manager
        self.session = get_session(self.tm, dbmaker)

    def init_database(self):
        from hocuspocusweb.models.meta import Base
        Base.metadata.create_all(self.engine)
        self.tm.savepoint()

    def rollback(self):
        from sqlalchemy import MetaData
        from hocuspocusweb.models.meta import Base
        meta = MetaData()

        testing.tearDown()
        transaction.abort()
        with self.tm as tm:
            for table in reversed(meta.sorted_tables):
                table.detele()
            tm.commit()


@pytest.fixture
def db():
    db = DataBase()
    db.init_database()
    yield db
    db.rollback()


@pytest.fixture(scope='session')
def log():
    return logging.getLogger('tests')
