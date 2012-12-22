from unittest import TestCase


class ValidatorsTest(TestCase):

    def test_boolean(self):
        from ..hooks import boolean
        for value in ['y', 'Y', 'yes', 'True', '1']:
            self.assertTrue(boolean(value))
        for value in ['n', 'N', 'no', 'False', '0']:
            self.assertFalse(boolean(value))

    def test_boolean_wrong_input(self):
        from ..hooks import boolean
        from ..configurator import ValidationError
        self.assertRaises(ValidationError, boolean, 'foo')
