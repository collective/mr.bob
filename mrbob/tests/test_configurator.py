import unittest
import os


class resolve_dottedTest(unittest.TestCase):

    def call_FUT(self, name):
        from ..configurator import resolve_dotted
        return resolve_dotted(name)

    def test_nomodule(self):
        self.assertRaises(ImportError, self.call_FUT, 'foobar.blabla:foo')

    def test_return_abs_path(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        abs_path = self.call_FUT('mrbob.tests:templates')
        self.assertEquals(abs_path, template_dir)


class parse_templateTest(unittest.TestCase):

    def call_FUT(self, name):
        from ..configurator import parse_template
        return parse_template(name)

    def test_relative(self):
        old_cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        abs_path = self.call_FUT('templates')
        os.chdir(old_cwd)
        self.assertEqual(abs_path, template_dir)

    def test_absolute(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        abs_path = self.call_FUT(template_dir)
        self.assertEqual(abs_path, template_dir)

    def test_dotted(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        abs_path = self.call_FUT('mrbob.tests:templates')
        self.assertEqual(abs_path, template_dir)

    def test_not_a_dir(self):
        self.assertRaises(ValueError, self.call_FUT, 'foo_bar')


#class ConfiguratorTest(unittest.TestCase):

#    def call_FUT(self, *args, **kw):
#        from ..configurator import Configurator
#        return Configurator(*args, **kw)

#    def test_foobar(self):
#        self.call_FUT()
