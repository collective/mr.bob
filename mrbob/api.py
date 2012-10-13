import ConfigParser as ConfigParser_


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


class ConfigParser(ConfigParser_.SafeConfigParser):
    """ a ConfigParser that can provide its values as simple dictionary.
    taken from http://stackoverflow.com/questions/3220670
    """

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


def config_from_file(fs_config, factory=Context):
    parser = ConfigParser(allow_no_value=True)
    parser.read(fs_config)
    return factory(**parser.as_dict())
