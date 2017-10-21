from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_tween(
        'hocuspocusweb.tweens.pid_tween_factory.pid_tween_factory')
    config.add_tween((
        'hocuspocusweb.tweens.'
        'error_file_tween_factory.error_file_tween_factory'))
    config.include('pyramid_jinja2')
    config.include('.models.meta')
    config.include('.session_io')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.scan()
    return config.make_wsgi_app()
