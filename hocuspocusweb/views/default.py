import logging

from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from sqlalchemy.orm.exc import NoResultFound

from ..models.user import User
from ..forms.open_door import OpenDoorForm


log = logging.getLogger(__name__)


@view_defaults(route_name='index')
class Index:

    def __init__(self, request):
        self.request = request

    @view_config(renderer='json',
                 attr='post',
                 request_method='POST')
    def post(self):

        ip_address = self.request.client_addr
        query = self.request.dbsession.query(User)
        log.info('ip address: {}'.format(ip_address))
        try:
            query.filter(User.ip_address == ip_address).one()
        except NoResultFound:
            self.request.response.status = 403
            return {'message': 'User not found'}

        password = self.request.POST['password']

        data = {
            'ip_address': ip_address,
            'password': password,
        }

        form = OpenDoorForm(self.request.dbsession, data=data)

        if form.validate():
            log.info('Door pid: {}'.format(self.request.door_pid))

            try:
                pid = int(self.request.door_pid)
            except ValueError:
                self.request.response.status = 500
                return {'message': 'Internal Error, PID is not an int.'}

            try:
                self.request.signal_usr1(pid)
            except ProcessLookupError:
                message = 'Process not found! Are you sure it is running?'
                self.request.response.status = 500
                return {'message': message}
            else:
                return {'message': 'Success!'}

        return {'errors': form.errors}
