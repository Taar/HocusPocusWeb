import os
import signal


def signal_usr1(pid):
    os.kill(pid, signal.SIGUSR1),


def dev_signal_usr1(pid):
    print('Signal was sent to: {} but not really'.format(pid))


def includeme(config):
    settings = config.get_settings()

    if settings['environment']:
        fn = dev_signal_usr1
    else:
        fn = signal_usr1

    config.add_request_method(
        lambda r: fn,
        'signal_usr1',
        reify=True
    )
