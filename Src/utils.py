class Dispatcher(object):
    """For doing single dispatch across arbitrary keys ... which we seem to do a lot of in this program."""
    def __init__(self, key: callable=None, default: callable=None):
        self.registry = {}
        self.key = key or self.pass_through
        self.default = default or self.pass_through

    def __call__(self, *args, **kwargs):
        try:
            method = self.registry[self.key(*args, **kwargs)]
        except KeyError:
            method = self.default

        return method(*args, **kwargs)

    def register(self, key):
        def decorator(method):
            self.registry[key] = method
            return method

        return decorator

    @staticmethod
    def pass_through(obj):
        return obj
