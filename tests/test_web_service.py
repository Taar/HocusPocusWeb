import pytest

from pyramid import testing
from .spy import Spy, Call


def dummy_request(dbsession, door_pid, signal_usr1_fn):
    return testing.DummyRequest(
        dbsession=dbsession,
        door_pid=door_pid,
        signal_usr1=signal_usr1_fn
    )


class TestMyView():

    @pytest.fixture(autouse=True)
    def transaction(self, request, db):
        db.init_database()
        request.addfinalizer(db.rollback)

    def test_user_not_found(self, db):
        from hocuspocusweb.views.default import Index

        signal_usr1_spy = Spy()
        index = Index(dummy_request(db.session, '101010101', signal_usr1_spy))
        index.request.client_addr = ''
        response = index.post()
        assert not signal_usr1_spy.called
        assert response == {'message': 'User not found'}

    def test_successful(self, db):
        from hocuspocusweb.models.user import User
        from hocuspocusweb.views.default import Index

        user = User(
            ip_address='192.168.1.111',
            mac_address='XX:XX:XX:XX:XX:XX:XX',
            name='Randy',
            password='somepassword',
            email='fake@fake.com'
        )
        db.session.add(user)

        signal_usr1_spy = Spy()
        index = Index(dummy_request(db.session, '101010101', signal_usr1_spy))
        index.request.client_addr = '192.168.1.111'
        index.request.POST = {'password': 'somepassword'}

        response = index.post()
        assert signal_usr1_spy.called
        assert signal_usr1_spy.count == 1
        assert signal_usr1_spy.calledWith(0) == Call({}, (101010101,))
        assert response == {'message': 'Success!'}

    def test_invalid_credentails(self, db):
        from hocuspocusweb.models.user import User
        from hocuspocusweb.views.default import Index

        user = User(
            ip_address='192.168.1.111',
            mac_address='XX:XX:XX:XX:XX:XX:XX',
            name='Randy',
            password='somepassword',
            email='fake@fake.com'
        )
        db.session.add(user)

        signal_usr1_spy = Spy()
        index = Index(dummy_request(db.session, '101010101', signal_usr1_spy))
        index.request.client_addr = '192.168.1.111'
        index.request.POST = {'password': 'differentpassword'}

        response = index.post()
        assert not signal_usr1_spy.called
        assert signal_usr1_spy.count == 0
        assert response == {
            'errors': {
                'password': ['Invalid Credentials.']
            }
        }

    def test_pid_not_a_number(self, db):
        from hocuspocusweb.models.user import User
        from hocuspocusweb.views.default import Index

        user = User(
            ip_address='192.168.1.111',
            mac_address='XX:XX:XX:XX:XX:XX:XX',
            name='Randy',
            password='somepassword',
            email='fake@fake.com'
        )
        db.session.add(user)

        signal_usr1_spy = Spy()
        index = Index(dummy_request(db.session, 'notanumber', signal_usr1_spy))
        index.request.client_addr = '192.168.1.111'
        index.request.POST = {'password': 'somepassword'}

        response = index.post()
        assert not signal_usr1_spy.called
        assert signal_usr1_spy.count == 0
        assert response == {'message': 'Internal Error, PID is not an int.'}

    def test_process_lookup_error(self, db):
        from hocuspocusweb.models.user import User
        from hocuspocusweb.views.default import Index

        user = User(
            ip_address='192.168.1.111',
            mac_address='XX:XX:XX:XX:XX:XX:XX',
            name='Randy',
            password='somepassword',
            email='fake@fake.com'
        )
        db.session.add(user)

        signal_usr1_spy = Spy(throw=ProcessLookupError)
        index = Index(dummy_request(db.session, '101010101', signal_usr1_spy))
        index.request.client_addr = '192.168.1.111'
        index.request.POST = {'password': 'somepassword'}

        response = index.post()
        assert signal_usr1_spy.called
        assert signal_usr1_spy.count == 1
        assert signal_usr1_spy.calledWith(0) == Call({}, (101010101,))
        assert response == {
            'message': 'Process not found! Are you sure it is running?'}
