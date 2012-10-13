import ConfigParser as ConfigParser_


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


def config_from_file(fs_config):
    parser = ConfigParser(allow_no_value=True)
    parser.read(fs_config)
    return parser.as_dict()
