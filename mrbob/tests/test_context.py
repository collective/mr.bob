from os import path
from mrbob.context import config_from_file


def test_parse_from_file():
    config = config_from_file(path.join(path.dirname(__file__), 'example.ini'))
    assert config['host']['ip_addr'] == '10.0.10.120'
