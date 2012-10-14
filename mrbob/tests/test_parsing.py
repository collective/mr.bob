from os import path
from py.test import mark, raises
from mrbob.parsing import parse_config

# py.test markers (see http://pytest.org/latest/example/markers.html)
config = mark.config


def make_one(fs_filename):
    import mrbob
    return path.abspath(path.join(path.dirname(mrbob.__file__),
        'tests', fs_filename))


def pytest_funcarg__parsed_config(request):
    def setup():
        if 'config' in request.keywords:
            fs_filename = request.keywords['config'].args[0]
        else:
            fs_filename = 'example.ini'
        return parse_config(make_one(fs_filename))

    return request.cached_setup(setup=setup,
        scope='function')


def test_parse_variable(parsed_config):
    assert parsed_config['variables']['name'] == 'Bob'


def test_parse_nested_variable(parsed_config):
    assert parsed_config['variables']['host']['ip_addr'] == '10.0.10.120'


def test_parse_2nd_level_nested_variable(parsed_config):
    assert parsed_config['variables']['webserver']['foo']['bar'] == 'barf'


@config('example2.ini')
def test_parse_nested_variable_out_of_order(parsed_config):
    assert parsed_config['variables']['webserver']['foo']['bar'] == 'barf2'
    assert parsed_config['variables']['webserver']['ip_addr'] == '127.0.0.3'


@config('example5.ini')
def test_parse_deeply_nested_variables(parsed_config):
    expected_config = {
        'mr.bob': {},
        'variables': {'a': {'b': {'c': {'d': 'foo', 'f': 'bar'}}}, 'name': 'Bob'},
        'questions': {},
    }
    assert parsed_config == expected_config


def test_overwrite_dict_with_value():
    """ providing a value for a key that already contains a
    dictionary raises a ConfigurationError """
    from ..configurator import ConfigurationError
    with raises(ConfigurationError):
        parse_config(make_one('example3.ini'))


def test_overwrite_value_with_dict():
    """ providing a dict for a key that already contains a
    string raises a ConfigurationError """
    from ..configurator import ConfigurationError
    with raises(ConfigurationError):
        parse_config(make_one('example4.ini'))


@config('example5.ini')
def test_parse_config_deeply_nested_structure(parsed_config):
    from ..parsing import pretty_format_config
    output = pretty_format_config(parsed_config['variables'])
    expected_output = [
        'a.b.c.d = foo',
        'a.b.c.f = bar',
        'name = Bob',
    ]
    assert output == expected_output


def test_parse_config(parsed_config):
    from ..parsing import pretty_format_config
    output = pretty_format_config(parsed_config['variables'])
    expected_output = [
        'host.ip_addr = 10.0.10.120',
        'name = Bob',
        'webserver.foo.bar = barf',
        'webserver.fqdn = mrbob.10.0.10.120.xip.io',
        'webserver.ip_addr = 127.0.0.2',
    ]
    assert output == expected_output


def test_update_config_override_one_option():
    from ..parsing import update_config
    config = {
        'foo': 'bar',
        'foo1': 'mar'
    }
    new_config = {
        'foo1': 'bar'
    }
    update_config(config, new_config)

    expected_config = {
        'foo': 'bar',
        'foo1': 'bar'
    }

    assert config == expected_config


def test_update_config_override_nested():
    from ..parsing import update_config
    config = {
        'foo': 'bar',
        'bar': {
            'foo': 'bar',
            'foo1': 'foo',
        }
    }
    new_config = {
        'foo1': 'bar',
        'bar': {
            'foo1': 'moo',
            'moo': 'moo',
        }
    }
    update_config(config, new_config)

    expected_config = {
        'foo': 'bar',
        'foo1': 'bar',
        'bar': {
            'foo': 'bar',
            'foo1': 'moo',
            'moo': 'moo',
        }
    }

    assert config == expected_config
