from unittest import TestCase
import mock


from .test_configurator import DummyConfigurator


class to_booleanTest(TestCase):

    def call_FUT(self, answer, configurator=None, question=None):
        from ..hooks import to_boolean
        return to_boolean(configurator or DummyConfigurator(), question, answer)

    def test_boolean(self):
        for value in ['y', 'Y', 'yes', 'True', '1']:
            self.assertTrue(self.call_FUT(value))
        for value in ['n', 'N', 'no', 'False', '0']:
            self.assertFalse(self.call_FUT(value))

    def test_boolean_wrong_input(self):
        from ..configurator import ValidationError
        self.assertRaises(ValidationError, self.call_FUT, 'foo')


class show_messageTest(TestCase):

    def call_FUT(self, configurator=None):
        from ..hooks import show_message
        return show_message(configurator)

    @mock.patch('sys.stdout')
    def test_hook_no_msg(self, mock_stdout):
        c = DummyConfigurator()
        self.call_FUT(c)
        self.assertEquals(mock_stdout.mock_calls, [])

    @mock.patch('sys.stdout')
    def test_hook_msg_formatting(self, mock_stdout):
        c = DummyConfigurator(variables={'foo': 'bar'},
                              templateconfig={'message': 'Hello %(foo)s!'})
        self.call_FUT(c)
        mock_stdout.write.assert_any_call('Hello bar!')

    @mock.patch('sys.stdout')
    def test_hook_quiet(self, mock_stdout):
        c = DummyConfigurator(variables={'foo': 'bar'},
                              quiet=True,
                              templateconfig={'message': 'Hello %(foo)s!'})
        self.call_FUT(c)
        self.assertEquals(mock_stdout.mock_calls, [])
