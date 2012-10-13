class Context(dict):
    """A dict-like representation of a to-be-rendered context.

    """

    name = ""

    def __getitem__(self, attr):
        try:
            return super(Context, self).__getitem__(attr)
        except KeyError:
            try:
                return getattr(self, attr)
            except AttributeError:
                raise KeyError

    def __setitem__(self, key, value, force=False):
        if force:
            super(Context, self).__setitem__(key, value)
        else:
            raise KeyError

    def __init__(self, **config):
        for key, value in config.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                self.__setitem__(key, value, force=True)
