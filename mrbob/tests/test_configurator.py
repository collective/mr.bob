# -*- coding: utf-8 -*-

import unittest
import os
import sys
import tempfile
import shutil
import six
from unittest import mock


mocked_pre_ask_question = mock.Mock()
mocked_post_ask_question = mock.Mock()
mocked_post_ask_question_validationerror = mock.Mock()
mocked_post_ask_question_validationerror_non_interactive = mock.Mock()
mocked_render_hook = mock.Mock()
mocked_ask_hook = mock.Mock()


def dummy_prompt(value):  # pragma: no cover
    pass


def dummy_renderer(value):  # pragma: no cover
    pass


def dummy_question_hook(configurator, question):  # pragma: no cover
    return


def dummy_question_hook2(configurator, question):  # pragma: no cover
    return


def dummy_render_hook(configurator):  # pragma: no cover
    return


def dummy_question_hook_skipquestion(configurator, question):  # pragma: no cover
    from ..bobexceptions import SkipQuestion
    raise SkipQuestion


class DummyConfigurator(object):
    def __init__(self,
                 defaults=None,
                 bobconfig=None,
                 templateconfig=None,
                 variables=None,
                 quiet=False):
        self.defaults = defaults or {}
        self.bobconfig = bobconfig or {}
        self.variables = variables or {}
        self.quiet = quiet
        self.templateconfig = templateconfig or {}


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
        from ..bobexceptions import ConfigurationError
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
        from ..bobexceptions import ConfigurationError
        self.assertRaises(ConfigurationError, self.call_FUT, 'foo_bar')

    @mock.patch('mrbob.configurator.urlretrieve')
    def test_zipfile(self, mock_urlretrieve):
        mock_urlretrieve.side_effect = self.fake_zip
        abs_path = self.call_FUT('http://foobar.com/bla.zip')
        self.assertEqual(set(os.listdir(abs_path[0])),
                         set(['test', '.mrbob.ini']))

    @mock.patch('mrbob.configurator.urlretrieve')
    def test_zipfile_base_path(self, mock_urlretrieve):
        mock_urlretrieve.side_effect = self.fake_zip_base_path
        abs_path = self.call_FUT('http://foobar.com/bla.zip#some/dir')
        self.assertEqual(set(os.listdir(abs_path[0])),
                         set(['test', '.mrbob.ini']))

    @mock.patch('mrbob.configurator.urlretrieve')
    def test_zipfile_not_zipfile(self, mock_urlretrieve):
        from ..bobexceptions import ConfigurationError
        mock_urlretrieve.side_effect = self.fake_wrong_zip
        self.assertRaises(ConfigurationError, self.call_FUT, 'http://foobar.com/bla.tar#some/dir')

    def fake_wrong_zip(self, url, path):
        with open(path, 'w') as f:
            f.write('boo')

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

    def test_target_directory_inside_template_dir(self):
        from ..bobexceptions import ConfigurationError
        self.assertRaises(ConfigurationError,
                          self.call_FUT,
                          'mrbob.tests:templates/questions1',
                          os.path.join(os.path.dirname(__file__), 'templates/questions1/foo'),
                          {})

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
        self.call_FUT('mrbob.tests:templates/empty2',
                      self.target_dir,
                      {})

    def test_parse_questions_extra_parameter(self):
        c = self.call_FUT(
            'mrbob.tests:templates/questions3',
            self.target_dir,
            {})
        self.assertEqual(c.questions[0].extra, {'foobar': 'something'})

    def test_parse_questions_all(self):
        c = self.call_FUT('mrbob.tests:templates/questions4',
                          self.target_dir,
                          {})
        self.assertEqual(len(c.questions), 1)
        self.assertEqual(c.questions[0].name, six.u('foo'))
        self.assertEqual(c.questions[0].default, "True")
        self.assertEqual(c.questions[0].required, False)
        self.assertEqual(c.questions[0].help, six.u('Blabla blabal balasd a a sd'))
        self.assertEqual(c.questions[0].command_prompt, dummy_prompt)

    def test_ask_questions_empty(self):
        args = ['mrbob.tests:templates/questions1',
                self.target_dir,
                {}]
        c = self.call_FUT(*args)
        c.questions = []
        c.variables = {}
        c.ask_questions()
        self.assertEquals(c.variables, {})

    def test_pre_post_ask_hooks_multiple(self):
        c = self.call_FUT(
            'mrbob.tests:templates/ask_hooks',
            self.target_dir,
            {},
        )
        self.assertEqual(c.pre_ask, [dummy_render_hook, mocked_ask_hook])
        self.assertEqual(c.post_ask, [dummy_render_hook, mocked_ask_hook])
        c.ask_questions()
        self.assertEqual(mocked_ask_hook.mock_calls, [mock.call(c), mock.call(c)])

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

    @mock.patch('mrbob.configurator.render_structure')
    def test_remember_answers(self, mock_render_structure):
        args = ['mrbob.tests:templates/questions1',
                self.target_dir,
                {'remember_answers': 'True'},
                {'foo.bar': '3'}]
        c = self.call_FUT(*args)
        c.render()
        with open(os.path.join(self.target_dir, '.mrbob.ini')) as f:
            self.assertEquals(f.read().strip(), """[variables]\nfoo.bar = 3""".strip())

    @mock.patch('mrbob.configurator.render_structure')
    def test_remember_answers_default(self, mock_render_structure):
        c = self.call_FUT(
            'mrbob.tests:templates/questions1',
            self.target_dir,
            variables={'foo.bar': '3'},
        )
        c.render()
        self.assertFalse(os.path.exists(os.path.join(self.target_dir, '.mrbob.ini')))

    def test_renderer_default(self):
        from ..rendering import jinja2_renderer
        c = self.call_FUT('mrbob.tests:templates/empty',
                      self.target_dir,
                      {})
        self.assertEqual(c.renderer, jinja2_renderer)

    def test_renderer_set(self):
        c = self.call_FUT('mrbob.tests:templates/renderer',
                      self.target_dir,
                      {})
        self.assertEqual(c.renderer, dummy_renderer)

    def test_pre_post_render_hooks_multiple(self):
        c = self.call_FUT(
            'mrbob.tests:templates/render_hooks',
            self.target_dir,
            {},
        )
        self.assertEqual(c.pre_render, [dummy_render_hook, mocked_render_hook])
        self.assertEqual(c.post_render, [dummy_render_hook, mocked_render_hook])
        c.render()
        self.assertEqual(mocked_render_hook.mock_calls, [mock.call(c), mock.call(c)])

    def test_ignored_files(self):
        c = self.call_FUT('mrbob.tests:templates/ignored',
                          self.target_dir,
                          {})
        self.assertEqual(len(c.ignored_files), 2)
        self.assertTrue('ignored' in c.ignored_files)
        self.assertTrue('*.txt' in c.ignored_files)

    def test_ignored_directories(self):
        c = self.call_FUT('mrbob.tests:templates/ignored_dirs',
                          self.target_dir,
                          {})
        self.assertEqual(len(c.ignored_directories), 2)
        self.assertTrue('ignored' in c.ignored_directories)
        self.assertTrue('*_stuff' in c.ignored_directories)


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
        self.assertEqual(q.command_prompt, moves.input)

    def test_repr(self):
        q = self.call_FUT('foo', 'Why?')
        self.assertEqual(repr(q), six.u("<Question name=foo question='Why?' default=None required=False>"))

    def test_ask(self):

        def cmd(q):
            self.assertEqual(q, '--> Why?: ')
            return 'foo'

        q = self.call_FUT('foo', 'Why?', command_prompt=cmd)
        answer = q.ask(DummyConfigurator())
        self.assertEqual(answer, 'foo')

    def test_ask_unicode(self):

        def cmd(q):
            self.assertTrue(isinstance(q, str))
            return 'foo'

        q = self.call_FUT('foo', six.u('č?'), command_prompt=cmd)
        q.ask(DummyConfigurator())

    def test_ask_default_empty(self):
        q = self.call_FUT('foo',
                          'Why?',
                          default="moo",
                          command_prompt=lambda x: '')
        answer = q.ask(DummyConfigurator())
        self.assertEqual(answer, 'moo')

    def test_ask_default_not_empty(self):

        def cmd(q):
            self.assertEqual(q, '--> Why? [moo]: ')
            return 'foo'

        q = self.call_FUT('foo',
                          'Why?',
                          default="moo",
                          command_prompt=cmd)
        answer = q.ask(DummyConfigurator())
        self.assertEqual(answer, 'foo')

    def test_ask_no_default_and_not_required(self):

        def cmd(q, go=['foo', '']):
            return go.pop()

        q = self.call_FUT('foo',
                          'Why?',
                          command_prompt=cmd)
        answer = q.ask(DummyConfigurator())
        self.assertEqual(answer, '')

    def test_ask_no_default_and_required(self):

        def cmd(q, go=['foo', '']):
            return go.pop()

        q = self.call_FUT('foo',
                          'Why?',
                          required=True,
                          command_prompt=cmd)
        answer = q.ask(DummyConfigurator())
        self.assertEqual(answer, 'foo')

    def test_ask_no_help(self):
        from six import StringIO

        def cmd(q, go=['foo', '?']):
            return go.pop()

        sys.stdout = StringIO()
        q = self.call_FUT('foo',
                          'Why?',
                          command_prompt=cmd)
        q.ask(DummyConfigurator())
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
        q.ask(DummyConfigurator())
        self.assertEqual(sys.stdout.getvalue(), 'foobar_help\n\n')
        sys.stdout = sys.__stdout__

    def test_non_interactive_required(self):
        from ..bobexceptions import ConfigurationError
        q = self.call_FUT('foo', 'Why?', required=True)
        c = DummyConfigurator(bobconfig={'non_interactive': 'True'})
        self.assertRaises(ConfigurationError, q.ask, c)

    def test_non_interactive_not_required(self):
        q = self.call_FUT('foo', 'Why?')
        c = DummyConfigurator(bobconfig={'non_interactive': 'True'})
        answer = q.ask(c)
        self.assertEquals(answer, '')

    def test_defaults_override(self):
        q = self.call_FUT('foo', 'Why?', default="foo")
        c = DummyConfigurator(bobconfig={'non_interactive': 'True'},
                              defaults={'foo': 'moo'})
        answer = q.ask(c)
        self.assertEquals(answer, 'moo')

    def test_pre_ask_question(self):
        q = self.call_FUT('foo',
                          'Why?',
                          command_prompt=lambda x: '',
                          pre_ask_question="mrbob.tests.test_configurator:mocked_pre_ask_question")
        c = DummyConfigurator()
        q.ask(c)
        mocked_pre_ask_question.assert_called_with(c, q)

    def test_pre_ask_question_multiple(self):
        q = self.call_FUT('foo', 'Why?', pre_ask_question="mrbob.tests.test_configurator:dummy_question_hook mrbob.tests.test_configurator:dummy_question_hook2")
        self.assertEqual(q.pre_ask_question, [dummy_question_hook, dummy_question_hook2])

    def test_pre_ask_question_skipquestion(self):
        q = self.call_FUT('foo', 'Why?', pre_ask_question="mrbob.tests.test_configurator:dummy_question_hook_skipquestion")
        self.assertEquals(q.ask(DummyConfigurator()), None)

    def test_post_ask_question(self):
        q = self.call_FUT('foo',
                          'Why?',
                          command_prompt=lambda x: '',
                          post_ask_question="mrbob.tests.test_configurator:mocked_post_ask_question")
        c = DummyConfigurator()
        answer = q.ask(c)
        mocked_post_ask_question.assert_called_with(c, q, '')
        self.assertEquals(mocked_post_ask_question(), answer)

    def test_post_ask_question_multiple(self):
        q = self.call_FUT('foo',
                          'Why?',
                          post_ask_question="mrbob.tests.test_configurator:dummy_question_hook mrbob.tests.test_configurator:dummy_question_hook2")
        self.assertEqual(q.post_ask_question,
                         [dummy_question_hook, dummy_question_hook2])

    def test_post_ask_question_validationerror(self):
        def cmd(q, go=['bar', 'foo']):
            return go.pop()

        def side_effect(configurator, question, answer):
            from ..bobexceptions import ValidationError
            if answer == 'foo':
                raise ValidationError
            elif answer == 'bar':
                return 'moo'

        mocked_post_ask_question_validationerror.side_effect = side_effect

        q = self.call_FUT('foo',
                          'Why?',
                          command_prompt=cmd,
                          post_ask_question="mrbob.tests.test_configurator:mocked_post_ask_question_validationerror")
        c = DummyConfigurator()
        self.assertEqual(q.ask(c), 'moo')

    def test_post_ask_question_validationerror_non_interactive(self):
        from ..bobexceptions import ConfigurationError, ValidationError

        mocked_post_ask_question_validationerror_non_interactive.side_effect = ValidationError

        q = self.call_FUT('foo',
                          'Why?',
                          command_prompt=lambda x: '',
                          post_ask_question="mrbob.tests.test_configurator:mocked_post_ask_question_validationerror_non_interactive")
        c = DummyConfigurator(bobconfig={'non_interactive': 'True'})
        self.assertRaises(ConfigurationError, q.ask, c)
