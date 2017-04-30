import pytest


class TestUser():

    @pytest.fixture(autouse=True)
    def transaction(self, db):
        db.init_database()
