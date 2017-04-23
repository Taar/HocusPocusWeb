from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from sqlalchemy.orm.exc import NoResultFound

from ..models.user import User
from ..forms.open_door import OpenDoorForm


@view_defaults(route_name='index')
class Index:

    def __init__(self, request):
        self.request = request

    @view_config(context=NoResultFound)
    def user_not_found(self):
        return Response('User not found',
                        content_type='text/plain',
                        status_int=403)

    @view_config(renderer='../templates/index.jinja2',
                 attr='get',
                 request_method='GET')
    def get(self):
        return {}

    @view_config(renderer='../templates/index.jinja2',
                 attr='post',
                 request_method='POST')
    def post(self):

        ip_address = self.request.client_addr
        query = self.request.dbsession.query(User)
        print('ip address: {}'.format(ip_address))
        # will throw NoResultFound which will be handled in an Exception view
        query.filter(User.ip_address == ip_address).one()

        password = self.request.POST['password']

        data = {
            'ip_address': ip_address,
            'password': password,
        }

        form = OpenDoorForm(self.request.dbsession, data=data)

        if form.validate():
            print('Door pid: {}'.format(self.request.door_pid))
            try:
                self.request.signal_usr1(int(self.request.door_pid))
            except ValueError:
                return Response('Internal Error, PID is not a int.',
                                content_type='text/plain',
                                status_int=500)
            except ProcessLookupError:
                message = 'Process not found! Are you sure it is running?'
                return Response(message,
                                content_type='text/plain',
                                status_int=500)
            else:
                return render_to_response(
                    '../templates/unlock.jinja2',
                    {'message': 'Success! Door is unlocking ... :D'},
                    request=self.request
                )

        return {'form': form}
