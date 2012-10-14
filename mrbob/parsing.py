import collections
try:
    import configparser as ConfigParser_  # NOQA
except ImportError:
    import ConfigParser as ConfigParser_  # NOQA


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
    from .configurator import ConfigurationError
    nested = dict()
    for key, value in variables.items():
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
    config['variables'] = nest_variables(config.get('variables', {}))
    config['mr.bob'] = nest_variables(config.get('mr.bob', {}))
    config['questions'] = nest_variables(config.get('questions', {}))
    return config


def update_config(to_be_updated_config, new_config):
    for k, v in new_config.iteritems():
        if isinstance(v, collections.Mapping):
            r = update_config(to_be_updated_config.get(k, {}), v)
            to_be_updated_config[k] = r
        else:
            to_be_updated_config[k] = new_config[k]
    return to_be_updated_config


def pretty_format_config(config):
    l = []

    def format_config(dict_, namespace=''):
        for key, value in dict_.items():
            if namespace:
                namespace_new = namespace + ".%s" % key
            else:
                namespace_new = key
            if isinstance(value, dict):
                format_config(value, namespace=namespace_new)
            else:
                l.append("%s = %s" % (namespace_new, value))

    format_config(config)

    return sorted(l)
