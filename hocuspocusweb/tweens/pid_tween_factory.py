from pyramid.response import Response
from ..util.file_helpers import get_file_contents as gfc


def pid_tween_factory(handler, registry, get_file_contents=gfc):

    def tween(request):
        pid_path = request.registry.settings.get(
            'door_controller_pid_path',
            None
        )

        if not pid_path:
            return Response('PID path not set in config',
                            content_type='text/plain',
                            status_int=500)

        pid_file_contents = get_file_contents(pid_path)

        if pid_file_contents is None:
            message = 'PID file not found in file system! {}'.format(pid_path)
            return Response(message,
                            content_type='text/plain',
                            status_int=500)

        elif len(pid_file_contents) <= 0:
            message = 'Process ID not found in PID file! {}'.format(pid_path)
            return Response(message,
                            content_type='text/plain',
                            status_int=500)
        else:
            request.door_pid = pid_file_contents

        return handler(request)

    return tween
