import ConfigParser as ConfigParser_

from .configurator import ConfigurationError


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


def nest_variables(variables):
    nested = dict()
    for key, value in variables.iteritems():
        segments = key.split('.')
        location = nested
        for segment in segments[:-1]:
            if segment not in location:
                location[segment] = dict()
            location = location[segment]
            if not isinstance(location, dict):
                raise ConfigurationError('Cannot assign "%s" to "%s".' % (value, location))

        location[segments[-1]] = value
    return nested


def parse_config(fs_config):
    parser = ConfigParser()
    parser.read(fs_config)
    config = parser.as_dict()
    config['variables'] = nest_variables(config['variables'])
    return config
