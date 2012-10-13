from os import path
from pytest import raises
from mrbob.api import Context
from mrbob.api import config_from_file


class DummyContext(Context):

    @property
    def access_control(self):
        return '%s/16 allow' % self.host['ip_addr']


def test_property_dict_access():
    context = DummyContext(host=dict(ip_addr='10.0.1.1'))
    assert context['access_control'] == '10.0.1.1/16 allow'


def test_property_dict_access_override():
    """setting a value will override a context's property of the same name"""
    context = DummyContext(ip_addr='10.0.1.1', access_control='foo')
    assert context['access_control'] == 'foo'


def test_key_error_raised():
    context = DummyContext()
    with raises(KeyError):
        context['foo']


def test_attribute_error_raised():
    context = DummyContext()
    with raises(AttributeError):
        context.foo


def test_item_access_via_property():
    context = DummyContext(foo='bar')
    assert context.foo == 'bar'


def test_item_not_writable():
    context = DummyContext()
    with raises(KeyError):
        context['foo'] = 'bar'


def test_parse_from_file():
    config = config_from_file(path.join(path.dirname(__file__), 'example.ini'))
    assert config['host']['ip_addr'] == '10.0.10.120'


def test_parse_from_file_with_custom_factory():
    config = config_from_file(path.join(path.dirname(__file__), 'example.ini'), factory=DummyContext)
    assert config['access_control'] == '10.0.10.120/16 allow'


def test_parse_from_file_with_custom_factory_override():
    config = config_from_file(path.join(path.dirname(__file__), 'example2.ini'), factory=DummyContext)
    assert config['access_control'] == {'bar': 'foo'}
