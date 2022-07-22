from unittest import TestCase
from unittest import mock
import time

from ..configurator import Question
from .test_configurator import DummyConfigurator


class to_booleanTest(TestCase):

    def call_FUT(self, answer, configurator=None, question=None):
        from ..hooks import to_boolean
        return to_boolean(
            configurator or DummyConfigurator(), question, answer)

    def test_boolean(self):
        for value in ['y', 'Y', 'yes', 'True', '1']:
            self.assertTrue(self.call_FUT(value))
        for value in ['n', 'N', 'no', 'False', '0']:
            self.assertFalse(self.call_FUT(value))

    def test_boolean_wrong_input(self):
        from ..bobexceptions import ValidationError
        self.assertRaises(ValidationError, self.call_FUT, 'foo')


class to_integerTest(TestCase):

    def call_FUT(self, answer, configurator=None, question=None):
        from ..hooks import to_integer
        return to_integer(
            configurator or DummyConfigurator(), question, answer)

    def test_integer(self):
        for value in [10, 415, -24, -1001, 0]:
            self.assertEquals(self.call_FUT(value), value)

    def test_integer_wrong_input(self):
        from ..bobexceptions import ValidationError
        self.assertRaises(ValidationError, self.call_FUT, 'foo')


class to_decimalTest(TestCase):

    def call_FUT(self, answer, configurator=None, question=None):
        from ..hooks import to_decimal
        return to_decimal(
            configurator or DummyConfigurator(), question, answer)

    def test_decimal(self):
        for value in [10.5, 10, 415.23, -24.0, -1001.231, 0, 0.0]:
            self.assertEquals(self.call_FUT(value), value)

    def test_decimal_wrong_input(self):
        from ..bobexceptions import ValidationError
        self.assertRaises(ValidationError, self.call_FUT, 'foo')


class validate_choicesTest(TestCase):

    def call_FUT(self, answer, configurator=None, question=None):
        from ..hooks import validate_choices
        return validate_choices(
            configurator or DummyConfigurator(), question, answer)

    def test_choices_default(self):
        q = Question(
            name='dummy', question='dummy', choices='MIT BSD Apache Other')
        self.assertEquals(self.call_FUT('bSd', question=q), 'bSd')

    def test_choices_default_wrong_input(self):
        from ..bobexceptions import ValidationError
        q = Question(
            name='dummy', question='dummy', choices='MIT BSD Apache Other')
        self.assertRaises(ValidationError, self.call_FUT, 'foo', None, q)

    def test_choices_case_sensitive(self):
        q = Question(
            name='dummy', question='dummy', choices='MIT BSD Apache Other',
            choices_case_sensitive='y')
        self.assertEquals(self.call_FUT('BSD', question=q), 'BSD')

    def test_choices_case_sensitive_wrong_input(self):
        from ..bobexceptions import ValidationError
        q = Question(
            name='dummy', question='dummy', choices='MIT BSD Apache Other',
            choices_case_sensitive='y')
        self.assertRaises(ValidationError, self.call_FUT, 'bsd', None, q)

    def test_choices_case_sensitive_invalid(self):
        q = Question(
            name='dummy', question='dummy', choices='MIT BSD Apache Other',
            choices_case_sensitive='allo')
        self.assertEquals(self.call_FUT('bsd', question=q), 'bsd')

    def test_choices_delimiter(self):
        q = Question(
            name='dummy', question='dummy', choices='MIT;BSD;Apache 2.0',
            choices_delimiter=';')
        self.assertEquals(
            self.call_FUT('apache 2.0', question=q), 'apache 2.0')

    def test_choices_delimiter_wrong_input(self):
        from ..bobexceptions import ValidationError
        q = Question(
            name='dummy', question='dummy', choices='MIT;BSD;Apache 2.0',
            choices_delimiter=';')
        self.assertRaises(ValidationError, self.call_FUT, 'mit;bsd', None, q)

    def test_choices_missing(self):
        q = Question(name='dummy', question='dummy')
        self.assertEquals(self.call_FUT('MIT', question=q), 'MIT')


class validate_regexTest(TestCase):

    def call_FUT(self, answer, configurator=None, question=None):
        from ..hooks import validate_regex
        return validate_regex(
            configurator or DummyConfigurator(), question, answer)

    def test_regex(self):
        q = Question(name='dummy', question='dummy', regex='^[a-z]+[0-9]+$')
        self.assertEquals(self.call_FUT('abc123', question=q), 'abc123')

    def test_regex_wrong_input(self):
        from ..bobexceptions import ValidationError
        q = Question(name='dummy', question='dummy', regex='^[a-z]+[0-9]+$')
        self.assertRaises(ValidationError, self.call_FUT, 'Wr0ng', None, q)

    def test_regex_missing(self):
        q = Question(name='dummy', question='dummy')
        self.assertEquals(self.call_FUT('abc123', question=q), 'abc123')


class set_current_datetimeTest(TestCase):

    def call_FUT(self, configurator=None, question=None):
        from ..hooks import set_current_datetime
        return set_current_datetime(
            configurator or DummyConfigurator(), question)

    def test_set_datetime_default(self):
        q = Question(name='dummy', question='dummy')
        self.call_FUT(question=q)
        self.assertEquals(q.default, time.strftime('%Y-%m-%d'))

    def test_set_datetime_custom(self):
        q = Question(name='dummy', question='dummy', datetime_format='%Y')
        self.call_FUT(question=q)
        self.assertEquals(q.default, time.strftime('%Y'))


class validate_datetimeTest(TestCase):

    def call_FUT(self, answer, configurator=None, question=None):
        from ..hooks import validate_datetime
        return validate_datetime(
            configurator or DummyConfigurator(), question, answer)

    def test_validate_datetime_default(self):
        q = Question(name='dummy', question='dummy')
        self.assertEquals(
            self.call_FUT('2014-03-01', question=q), '2014-03-01')

    def test_validate_datetime_default_wrong_input(self):
        from ..bobexceptions import ValidationError
        q = Question(name='dummy', question='dummy')
        self.assertRaises(ValidationError, self.call_FUT, 'foo', None, q)

    def test_validate_datetime_custom(self):
        q = Question(name='dummy', question='dummy', datetime_format='%Y')
        self.assertEquals(
            self.call_FUT('2014', question=q), '2014')

    def test_validate_datetime_custom_wrong_input(self):
        from ..bobexceptions import ValidationError
        q = Question(name='dummy', question='dummy', datetime_format='%Y')
        self.assertRaises(ValidationError, self.call_FUT, 'foo', None, q)


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
