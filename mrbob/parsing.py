import collections
try:  # pragma: no cover
    from collections import OrderedDict  # NOQA
except ImportError:  # pragma: no cover
    from ordereddict import OrderedDict  # NOQA
from six.moves import configparser
from six import PY3


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
                raise ConfigurationError('Cannot assign "%s" to group "%s", subgroup is already used.' % (value, key))

        if PY3:  # pragma: no cover
            location[segments[-1]] = value
        else:  # pragma: no cover
            location[segments[-1]] = value.decode('utf-8')
    return nested


def parse_config(fs_config):
    parser = configparser.SafeConfigParser(dict_type=OrderedDict)
    parser.read(fs_config)
    config = dict()
    for section in ['variables', 'defaults', 'mr.bob', 'questions', 'template']:
        if parser.has_section(section):
            items = parser.items(section)
            if section == 'questions':
                config[section + "_order"] = [key[:-9] for key, value in items if key.endswith('question')]
            if section in ['variables', 'defaults']:
                if PY3:  # pragma: no cover
                    config[section] = dict(items)
                else:  # pragma: no cover
                    config[section] = dict([(key, value.decode('utf-8')) for key, value in items])
            else:
                config[section] = nest_variables(dict(items))
        else:
            config[section] = {}
    return config


def write_config(fs_config, section, data):
    parser = configparser.SafeConfigParser(dict_type=OrderedDict)
    parser.add_section(section)
    for key, value in data.items():
        if not PY3:  # pragma: no cover
            value = value.encode('utf-8')
        parser.set(section, key, value)
    with open(fs_config, 'w') as f:
        parser.write(f)


def update_config(first_config, second_config):
    for k, v in second_config.items():
        if isinstance(v, collections.Mapping):
            r = update_config(first_config.get(k, {}), v)
            first_config[k] = r
        else:
            first_config[k] = second_config[k]
    return first_config


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
