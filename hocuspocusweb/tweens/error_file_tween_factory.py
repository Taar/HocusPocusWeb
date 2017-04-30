from pyramid.response import Response
from ..util.file_helpers import get_file_contents as gfc


def error_file_tween_factory(
        handler, registry, get_file_contents=gfc):

    def tween(request):
        error_path = request.registry.settings.get(
            'door_controller_error_path',
            None
        )

        if not error_path:
            return Response(json={'message': 'Error path not set in config'},
                            content_type='application/json',
                            status_int=500)

        error_file_contents = get_file_contents(error_path)

        if error_file_contents is not None:

            return Response(json={'message': error_file_contents},
                            content_type='application/json',
                            status_int=500)

        return handler(request)

    return tween
