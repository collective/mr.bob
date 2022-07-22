import os
import tempfile
import collections
try:  # pragma: no cover
    from collections import OrderedDict  # NOQA
except ImportError:  # pragma: no cover
    from ordereddict import OrderedDict  # NOQA
import six
from six.moves import configparser

try:  # pragma: no cover
    from urllib import urlretrieve  # NOQA
except ImportError:  # pragma: no cover
    # PY3K
    from urllib.request import urlretrieve  # NOQA

from .bobexceptions import ConfigurationError


def nest_variables(variables):
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

        k = segments[-1]
        if isinstance(location.get(k, None), dict):
            raise ConfigurationError('Cannot assign "%s" to group "%s", subgroup is already used.' % (value, k))
        if six.PY3:  # pragma: no cover
            location[k] = value
        else:  # pragma: no cover
            location[k] = value.decode('utf-8')
    return nested


def parse_config(configname):
    tmpfile = None
    if configname.startswith('http'):
        tmpfile = tempfile.NamedTemporaryFile()
        urlretrieve(configname, tmpfile.name)
        configname = tmpfile.name

    if not os.path.exists(configname):
        raise ConfigurationError('config file does not exist: %s' % configname)

    parser = configparser.SafeConfigParser(dict_type=OrderedDict)
    parser.read(configname)
    config = dict()
    for section in ['variables', 'defaults', 'mr.bob', 'questions', 'template']:
        if parser.has_section(section):
            items = parser.items(section)
            if section == 'questions':
                config[section + "_order"] = [key[:-9] for key, value in items if key.endswith('.question')]
            if section in ['variables', 'defaults']:
                if six.PY3:  # pragma: no cover
                    config[section] = dict(items)
                else:  # pragma: no cover
                    config[section] = dict([(key, value.decode('utf-8')) for key, value in items])
            else:
                config[section] = nest_variables(dict(items))
        else:
            config[section] = {}

    if tmpfile:
        tmpfile.close()

    return config


def write_config(fs_config, section, data):
    parser = configparser.SafeConfigParser(dict_type=OrderedDict)
    parser.add_section(section)
    for key, value in data.items():
        if not isinstance(value, six.string_types):
            value = str(value)

        if not six.PY3:  # pragma: no cover
            value = value.encode('utf-8')
        parser.set(section, key, value)
    with open(fs_config, 'w') as f:
        parser.write(f)


def update_config(first_config, second_config):
    for k, v in second_config.items():
        if isinstance(v, collections.abc.Mapping):
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
