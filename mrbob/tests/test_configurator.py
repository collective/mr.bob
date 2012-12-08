# -*- coding: utf-8 -*-

import unittest
import os
import sys
import tempfile
import shutil
import six
import mock


def dummy_validator(value):  # pragma: no cover
    pass


def dummy_action(value):  # pragma: no cover
    pass


def dummy_prompt(value):  # pragma: no cover
    pass


class resolve_dotted_pathTest(unittest.TestCase):

    def call_FUT(self, name):
        from ..configurator import resolve_dotted_path
        return resolve_dotted_path(name)

    def test_nomodule(self):
        self.assertRaises(ImportError, self.call_FUT, 'foobar.blabla:foo')

    def test_return_abs_path(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        abs_path = self.call_FUT('mrbob.tests:templates')
        self.assertEquals(abs_path, template_dir)


class resolve_dotted_funcTest(unittest.TestCase):

    def call_FUT(self, name):
        from ..configurator import resolve_dotted_func
        return resolve_dotted_func(name)

    def test_nomodule(self):
        self.assertRaises(ImportError, self.call_FUT, 'foobar.blabla:foo')

    def test_error_no_func(self):
        from ..configurator import ConfigurationError
        self.assertRaises(ConfigurationError, self.call_FUT, 'mrbob.rendering:foo')

    def test_return_func(self):
        from mrbob.rendering import jinja2_renderer
        func = self.call_FUT('mrbob.rendering:jinja2_renderer')
        self.assertEquals(func, jinja2_renderer)


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
        self.assertEqual(abs_path, (template_dir, False))

    def test_absolute(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        abs_path = self.call_FUT(template_dir)
        self.assertEqual(abs_path, (template_dir, False))

    def test_dotted(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        abs_path = self.call_FUT('mrbob.tests:templates')
        self.assertEqual(abs_path, (template_dir, False))

    def test_not_a_dir(self):
        from ..configurator import ConfigurationError
        self.assertRaises(ConfigurationError, self.call_FUT, 'foo_bar')

    @mock.patch('mrbob.configurator.urlretrieve')
    def test_zipfile(self, mock_urlretrieve):
        mock_urlretrieve.side_effect = self.fake_zip
        abs_path = self.call_FUT('http://foobar.com/bla.zip')
        self.assertEqual(os.listdir(abs_path[0]),
                         ['test', '.mrbob.ini'])

    @mock.patch('mrbob.configurator.urlretrieve')
    def test_zipfile_base_path(self, mock_urlretrieve):
        mock_urlretrieve.side_effect = self.fake_zip_base_path
        abs_path = self.call_FUT('http://foobar.com/bla.zip#some/dir')
        self.assertEqual(os.listdir(abs_path[0]),
                         ['test', '.mrbob.ini'])

    @mock.patch('mrbob.configurator.urlretrieve')
    def test_zipfile_not_zipfile(self, mock_urlretrieve):
        from ..configurator import ConfigurationError
        mock_urlretrieve.side_effect = self.fake_wrong_zip
        self.assertRaises(ConfigurationError, self.call_FUT, 'http://foobar.com/bla.tar#some/dir')

    def fake_wrong_zip(self, url, path):
        if six.PY3:  # pragma: no cover
            path.write(bytes('boo', 'utf-8'))
        else:  # pragma: no cover
            path.write('boo')

    def fake_zip(self, url, path):
        import zipfile
        zf = zipfile.ZipFile(path, 'w')
        try:
            zf.writestr('.mrbob.ini', '[questions]\n')
            zf.writestr('test', 'test')
        finally:
            zf.close()

    def fake_zip_base_path(self, url, path):
        import zipfile
        zf = zipfile.ZipFile(path, 'w')
        try:
            zf.writestr('some/dir/.mrbob.ini', '[questions]\n')
            zf.writestr('some/dir/test', 'test')
        finally:
            zf.close()


class ConfiguratorTest(unittest.TestCase):

    def setUp(self):
        self.target_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.target_dir)

    def call_FUT(self, *args, **kw):
        from ..configurator import Configurator
        return Configurator(*args, **kw)

    def test_parse_questions_basic(self):
        c = self.call_FUT('mrbob.tests:templates/questions1',
                          self.target_dir,
                          {})
        self.assertEqual(len(c.questions), 2)
        self.assertEqual(c.questions[0].name, 'foo.bar.car.dar')
        self.assertEqual(c.questions[0].question, 'Why?')
        self.assertEqual(c.questions[1].name, 'foo')
        self.assertEqual(c.questions[1].question, 'What?')

    def test_parse_questions_no_questions(self):
        c = self.call_FUT('mrbob.tests:templates/questions2',
                          self.target_dir,
                          {})
        self.assertEqual(len(c.questions), 0)

    def test_parse_questions_no_questions_section(self):
        # expected failure: KeyError: 'questions_order'
        self.call_FUT('mrbob.tests:templates/empty2',
                      self.target_dir,
                      {})

    def test_parse_questions_extra_parameter(self):
        from ..configurator import TemplateConfigurationError
        self.assertRaises(TemplateConfigurationError,
                          self.call_FUT,
                          'mrbob.tests:templates/questions3',
                          self.target_dir,
                          {})

    def test_parse_questions_all(self):
        c = self.call_FUT('mrbob.tests:templates/questions4',
                          self.target_dir,
                          {})
        self.assertEqual(len(c.questions), 1)
        self.assertEqual(c.questions[0].name, six.u('foo'))
        self.assertEqual(c.questions[0].default, "True")
        self.assertEqual(c.questions[0].required, False)
        self.assertEqual(c.questions[0].validator, dummy_validator)
        self.assertEqual(c.questions[0].help, six.u('Blabla blabal balasd a a sd'))
        self.assertEqual(c.questions[0].action, dummy_action)
        self.assertEqual(c.questions[0].command_prompt, dummy_prompt)

    def test_default_and_required(self):
        from ..configurator import TemplateConfigurationError
        args = ['mrbob.tests:templates/questions5',
                self.target_dir,
                {}]
        self.assertRaises(TemplateConfigurationError, self.call_FUT, *args)

    def test_ask_questions_empty(self):
        args = ['mrbob.tests:templates/questions1',
                self.target_dir,
                {}]
        c = self.call_FUT(*args)
        c.questions = []
        c.variables = {}
        c.ask_questions()
        self.assertEquals(c.variables, {})

    def test_ask_questions_missing(self):
        from ..configurator import Question
        args = ['mrbob.tests:templates/questions1',
                self.target_dir,
                {}]
        c = self.call_FUT(*args)
        c.questions = [Question('foo.bar', 'fobar?'), Question('moo', "Moo?", command_prompt=lambda x: 'moo.')]
        c.variables = {'foo.bar': 'answer'}
        c.ask_questions()
        self.assertEquals(c.variables, {'foo.bar': 'answer', 'moo': 'moo.'})


class QuestionTest(unittest.TestCase):

    def call_FUT(self, *args, **kw):
        from ..configurator import Question
        return Question(*args, **kw)

    def test_defaults(self):
        from six import moves
        q = self.call_FUT('foo', 'Why?')
        self.assertEqual(q.name, 'foo')
        self.assertEqual(q.default, None)
        self.assertEqual(q.required, False)
        self.assertEqual(q.help, "")
        self.assertEqual(q.validator, None)
        self.assertEqual(q.command_prompt, moves.input)

    def test_repr(self):
        q = self.call_FUT('foo', 'Why?')
        self.assertEqual(repr(q), six.u("<Question name=foo question='Why?' default=None required=False>"))

    def test_ask(self):

        def cmd(q):
            self.assertEqual(q, '--> Why?: ')
            return 'foo'

        q = self.call_FUT('foo', 'Why?', command_prompt=cmd)
        answer = q.ask()
        self.assertEqual(answer, 'foo')

    def test_ask_unicode(self):

        def cmd(q):
            self.assertTrue(isinstance(q, str))
            return 'foo'

        q = self.call_FUT('foo', six.u('č?'), command_prompt=cmd)
        q.ask()

    def test_ask_default_empty(self):
        q = self.call_FUT('foo',
                          'Why?',
                          default="moo",
                          command_prompt=lambda x: '')
        answer = q.ask()
        self.assertEqual(answer, 'moo')

    def test_ask_default_not_empty(self):

        def cmd(q):
            self.assertEqual(q, '--> Why? [moo]: ')
            return 'foo'

        q = self.call_FUT('foo',
                          'Why?',
                          default="moo",
                          command_prompt=cmd)
        answer = q.ask()
        self.assertEqual(answer, 'foo')

    def test_ask_no_default_and_not_required(self):

        def cmd(q, go=['foo', '']):
            return go.pop()

        q = self.call_FUT('foo',
                          'Why?',
                          command_prompt=cmd)
        answer = q.ask()
        self.assertEqual(answer, '')

    def test_ask_no_default_and_required(self):

        def cmd(q, go=['foo', '']):
            return go.pop()

        q = self.call_FUT('foo',
                          'Why?',
                          required=True,
                          command_prompt=cmd)
        answer = q.ask()
        self.assertEqual(answer, 'foo')

    def test_ask_no_help(self):
        from six import StringIO

        def cmd(q, go=['foo', '?']):
            return go.pop()

        sys.stdout = StringIO()
        q = self.call_FUT('foo',
                          'Why?',
                          command_prompt=cmd)
        q.ask()
        self.assertEqual(sys.stdout.getvalue(), 'There is no additional help text.\n\n')
        sys.stdout = sys.__stdout__

    def test_ask_help(self):
        from six import StringIO

        def cmd(q, go=['foo', '?']):
            return go.pop()

        sys.stdout = StringIO()
        q = self.call_FUT('foo',
                          'Why?',
                          help="foobar_help",
                          command_prompt=cmd)
        q.ask()
        self.assertEqual(sys.stdout.getvalue(), 'foobar_help\n\n')
        sys.stdout = sys.__stdout__

    def test_validator_no_return(self):
        q = self.call_FUT('foo',
                          'Why?',
                          validator=dummy_validator,
                          command_prompt=lambda x: 'foo')
        answer = q.ask()
        self.assertEqual(answer, 'foo')

    def test_validator_return(self):
        q = self.call_FUT('foo',
                          'Why?',
                          validator=lambda x: 'moo',
                          command_prompt=lambda x: 'foo')
        answer = q.ask()
        self.assertEqual(answer, 'moo')

    def test_validator_error(self):
        from ..configurator import ValidationError

        def cmd(q, go=['foo', 'moo']):
            return go.pop()

        def validator(value):
            if value != 'foo':
                raise ValidationError

        q = self.call_FUT('foo',
                          'Why?',
                          validator=validator,
                          command_prompt=cmd)
        answer = q.ask()
        self.assertEqual(answer, 'foo')
