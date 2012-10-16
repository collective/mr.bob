import unittest
import tempfile
import os


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
        self.assertRaises(SystemExit, self.call_FUT, 'foo')

    def test_dummy_template(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'empty')
        output_dir = tempfile.mkdtemp()
        self.call_FUT('-O', output_dir, template_dir)

    def test_dummy_template_create_target_directory(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'empty')
        output_dir = os.path.join(tempfile.mkdtemp(), 'notexist')
        self.call_FUT('-O', os.path.join(output_dir), template_dir)
        self.assertTrue(os.path.isdir(output_dir))

    def test_list_questions(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'empty')
        self.call_FUT('--list-questions', template_dir)

    def test_set_renderer(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'empty')
        self.call_FUT('--renderer', 'mrbob.rendering:python_formatting_renderer', template_dir)
        # TODO: assert renderer was used

    def test_missing_mrbobini_in_template(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'unbound', 'etc')
        output_dir = tempfile.mkdtemp()
        self.assertRaises(SystemExit, self.call_FUT, '-O', output_dir, template_dir)
