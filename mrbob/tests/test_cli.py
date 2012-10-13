import unittest


class TestCLI(unittest.TestCase):

    def call_FUT(self, *args):
        from ..cli import main
        return main(args)

    def test_version(self):
        output = self.call_FUT('--version')
        self.assertEqual(output, '0.1')

    def test_no_template(self):
        self.assertRaises(SystemExit, self.call_FUT)

    def test_template_render(self):
        self.call_FUT('foo')
