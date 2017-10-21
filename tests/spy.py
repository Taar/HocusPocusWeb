from collections import namedtuple


Call = namedtuple('Call', 'kwargs args')


class Spy:

    def __init__(self, **kwargs):
        self._throw = kwargs.get('throw', None)
        self._returns = kwargs.get('returns', None)
        self.count = 0
        self.called = False
        self._calls = []

    def __call__(self, *args, **kwargs):
        self.count += 1
        self.called = True
        self._calls.append(Call(kwargs, args))
        if self._throw:
            raise self._throw
        return self._returns

    def calledWith(self, index):
        return self._calls[index]
