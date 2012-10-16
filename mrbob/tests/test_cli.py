import unittest
import tempfile
import os
import shutil
import mock


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.output_dir)

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
        self.call_FUT('-O', self.output_dir, template_dir)

    @mock.patch('mrbob.cli.Configurator')
    def test_cleanup_tempdir(self, mock_Configurator):
        template_dir = tempfile.mkdtemp()
        mock_Configurator().is_tempdir.return_value = True
        mock_Configurator().template_dir = template_dir
        self.call_FUT(template_dir)
        self.assertFalse(os.path.exists(template_dir))

    def test_dummy_template_create_target_directory(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'empty')
        self.call_FUT('-O', os.path.join(self.output_dir, 'notexist'), template_dir)
        self.assertTrue(os.path.isdir(self.output_dir))

    def test_list_questions(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'empty')
        self.call_FUT('--list-questions', template_dir)

    def test_set_renderer(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'empty')
        self.call_FUT('--renderer', 'mrbob.rendering:python_formatting_renderer', template_dir)
        # TODO: assert renderer was used

    def test_missing_mrbobini_in_template(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'unbound', 'etc')
        self.assertRaises(SystemExit, self.call_FUT, '-O', self.output_dir, template_dir)

    def test_no_config_file(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'empty')
        self.assertRaises(SystemExit, self.call_FUT, '-c', '/notexists', template_dir)

    @mock.patch('mrbob.cli.os.path.expanduser')
    def test_configs_override_each_other(self, mock_expanduser):
        # global config
        globalconfig = tempfile.mkstemp()[1]
        mock_expanduser.return_value = globalconfig
        with open(globalconfig, 'w') as f:
            f.write("""
[mr.bob]
only_global = glob
overriden_by_file = foo

[variables]
only_global = glob
overriden_by_file = file

                    """)

        # config file
        tempconfig = tempfile.mkstemp()[1]
        with open(tempconfig, 'w') as f:
            f.write("""
[mr.bob]
only_file = file
overriden_by_file = file1

[variables]
only_file = file
overriden_by_file = file1
                    """)

        # TODO: also test cli parameters when it's implemented
        template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'multiconfig')
        self.call_FUT('-v',
                      '-O', self.output_dir,
                      '-c', tempconfig,
                      template_dir)
        with open(os.path.join(self.output_dir, 'vars')) as f:
            output = f.read()
            self.assertEquals(output, "glob\nfile\nfile1")

        # cleanup
        os.remove(tempconfig)
