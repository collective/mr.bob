import unittest


class TestCLI(unittest.TestCase):

    def call_FUT(self, *args):
        from ..cli import main
        return main(args)

    def test_version(self):
        output = self.call_FUT('--version')
        self.assertEqual(output, '0.1')

    def test_no_template_name(self):
        self.assertRaises(SystemExit, self.call_FUT)

    def test_no_template_directory(self):
        self.assertRaises(ValueError, self.call_FUT, 'foo')

    #def test_dummy_template(self):
    #    self.call_FUT()
