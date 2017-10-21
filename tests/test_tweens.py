import pytest

from pyramid import testing
from .spy import Spy, Call


class TestTweens():

    def test_error_file_tween_path_not_found(self):
        from hocuspocusweb.tweens.error_file_tween_factory import (
            error_file_tween_factory
        )
        request = testing.DummyRequest()
        config = testing.setUp(request=request)

        handler_spy = Spy(returns=request.response)
        error_file_tween = error_file_tween_factory(handler_spy, config)

        response = error_file_tween(request)
        assert not handler_spy.called
        assert response.status_code == 500
        assert response.content_type == 'application/json'
        assert response.json == {'message': 'Error path not set in config'}

    def test_error_file_tween_error_found(self):
        from hocuspocusweb.tweens.error_file_tween_factory import (
            error_file_tween_factory
        )
        request = testing.DummyRequest()
        settings = {'door_controller_error_path': 'not_a_real_file.txt'}
        config = testing.setUp(request=request, settings=settings)

        get_file_contents_spy = Spy(returns='Error!!!')
        handler_spy = Spy(returns=request.response)

        error_file_tween = error_file_tween_factory(
            handler_spy, config, get_file_contents=get_file_contents_spy)

        response = error_file_tween(request)
        assert not handler_spy.called
        assert response.status_code == 500
        assert response.content_type == 'application/json'
        assert response.json == {'message': 'Error!!!'}

    def test_error_file_tween_error_found(self):
        from hocuspocusweb.tweens.error_file_tween_factory import (
            error_file_tween_factory
        )
        request = testing.DummyRequest()
        settings = {'door_controller_error_path': 'not_a_real_file.txt'}
        config = testing.setUp(request=request, settings=settings)

        get_file_contents_spy = Spy(returns=None)
        handler_spy = Spy(returns=request.response)

        error_file_tween = error_file_tween_factory(
            handler_spy, config, get_file_contents=get_file_contents_spy)

        response = error_file_tween(request)
        assert handler_spy.called
        assert handler_spy.count == 1
        assert response.status_code == 200

    def test_pid_tween_pid_path_not_found(self):
        from hocuspocusweb.tweens.pid_tween_factory import (
            pid_tween_factory
        )
        request = testing.DummyRequest()
        config = testing.setUp(request=request)

        handler_spy = Spy(returns=request.response)
        get_file_contents_spy = Spy(returns=None)
        pid_tween = pid_tween_factory(
            handler_spy, config, get_file_contents_spy)

        response = pid_tween(request)
        assert not handler_spy.called
        assert response.status_code == 500
        assert response.content_type == 'application/json'
        assert response.json == {'message': 'PID path not set in config'}

    def test_pid_tween_pid_file_contents_returns_none(self):
        from hocuspocusweb.tweens.pid_tween_factory import (
            pid_tween_factory
        )
        request = testing.DummyRequest()
        settings = {'door_controller_pid_path': 'not_a_real_file.txt'}
        config = testing.setUp(request=request, settings=settings)

        handler_spy = Spy(returns=request.response)

        get_file_contents_spy = Spy(returns=None)

        pid_tween = pid_tween_factory(
            handler_spy, config, get_file_contents_spy)

        response = pid_tween(request)
        assert not handler_spy.called
        assert get_file_contents_spy.count == 1
        assert get_file_contents_spy.calledWith(0) == Call(
            {}, ('not_a_real_file.txt',))
        assert response.status_code == 500
        assert response.content_type == 'application/json'
        assert response.json == {
            'message': 'PID file not found in file system! not_a_real_file.txt'
        }

    def test_pid_tween_pid_file_contents_are_empty(self):
        from hocuspocusweb.tweens.pid_tween_factory import (
            pid_tween_factory
        )
        request = testing.DummyRequest()
        settings = {'door_controller_pid_path': 'not_a_real_file.txt'}
        config = testing.setUp(request=request, settings=settings)

        handler_spy = Spy(returns=request.response)

        get_file_contents_spy = Spy(returns='')

        pid_tween = pid_tween_factory(
            handler_spy, config, get_file_contents_spy)

        response = pid_tween(request)
        assert not handler_spy.called
        assert get_file_contents_spy.count == 1
        assert get_file_contents_spy.calledWith(0) == Call(
            {}, ('not_a_real_file.txt',))
        assert response.status_code == 500
        assert response.content_type == 'application/json'
        assert response.json == {
            'message': 'Process ID not found in PID file! not_a_real_file.txt'
        }

    def test_pid_tween_pid_file_contents_the_pid(self):
        from hocuspocusweb.tweens.pid_tween_factory import (
            pid_tween_factory
        )
        request = testing.DummyRequest()
        settings = {'door_controller_pid_path': 'not_a_real_file.txt'}
        config = testing.setUp(request=request, settings=settings)

        handler_spy = Spy(returns=request.response)

        get_file_contents_spy = Spy(returns='12345')

        pid_tween = pid_tween_factory(
            handler_spy, config, get_file_contents_spy)

        response = pid_tween(request)
        assert handler_spy.called
        assert get_file_contents_spy.count == 1
        assert get_file_contents_spy.calledWith(0) == Call(
            {}, ('not_a_real_file.txt',))
        assert response.status_code == 200
        assert request.door_pid == '12345'
