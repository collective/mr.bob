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


def test_overwrite_dict_with_value():
    """ providing a value for a key that already contains a
    dictionary raises a ValueError """
    with raises(ValueError):
        parse_config(make_one('example3.ini'))


def test_overwrite_value_with_dict():
    """ providing a dict for a key that already contains a
    string raises a ValueError """
    with raises(ValueError):
        parse_config(make_one('example4.ini'))
