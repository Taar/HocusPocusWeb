import pytest

from pyramid import testing
from .spy import Spy, Call


class TestTweens():

    def test_error_file_tween_path_not_found(self, log):
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

    def test_error_file_tween_error_found(self, log):
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

    def test_error_file_tween_error_found(self, log):
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
