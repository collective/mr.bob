""""""

import os
import re
import sys
import readline
try:  # pragma: no cover
    from urllib import urlretrieve  # NOQA
except ImportError:  # pragma: no cover
    # PY3K
    from urllib.request import urlretrieve  # NOQA
import tempfile
from zipfile import ZipFile, is_zipfile
readline  # make pyflakes happy, readline makes interactive mode keep history

import six
from importlib import import_module

from .rendering import render_structure
from .parsing import parse_config, update_config, pretty_format_config


DOTTED_REGEX = re.compile(r'^[a-zA-Z_.]+:[a-zA-Z_.]+$')


class MrBobError(Exception):
    """Base class for errors"""


class ConfigurationError(MrBobError):
    """Raised during configuration phase"""


class TemplateConfigurationError(ConfigurationError):
    """Raised reading template configuration"""


class ValidationError(MrBobError):
    """Raised during question validation"""


def resolve_dotted_path(name):
    module_name, dir_name = name.rsplit(':', 1)
    module = import_module(module_name)
    return os.path.join(os.path.dirname(module.__file__), dir_name)


def resolve_dotted_func(name):
    module_name, func_name = name.split(':')
    module = import_module(module_name)
    func = getattr(module, func_name, None)
    if func:
        return func
    else:
        raise ConfigurationError("There is no object named %s in module %s" % (module_name, func_name))


def maybe_resolve_dotted_func(name):
    if isinstance(name, six.string_types) and DOTTED_REGEX.match(name):
        return resolve_dotted_func(name)
    else:
        return name


def maybe_bool(value):
    if value == "True":
        return True
    if value == "False":
        return False
    else:
        return value


def parse_template(template_name):
    """Resolve template name into absolute path to the template
    and boolean if absolute path is temporary directory.
    """
    if template_name.startswith('http'):
        if '#' in template_name:
            url, subpath = template_name.rsplit('#', 1)
        else:
            url = template_name
            subpath = ''
        with tempfile.NamedTemporaryFile() as tmpfile:
            urlretrieve(url, tmpfile)
            if not is_zipfile(tmpfile.name):
                raise ConfigurationError("Not a zip file: %s" % tmpfile)
            zf = ZipFile(tmpfile)
            try:
                path = tempfile.mkdtemp()
                zf.extractall(path)
                return os.path.join(path, subpath), True
            finally:
                zf.close()

    if ':' in template_name:
        path = resolve_dotted_path(template_name)
    else:
        path = os.path.realpath(template_name)

    if not os.path.isdir(path):
        raise ConfigurationError('Template directory does not exist: %s' % path)
    return path, False


class Configurator(object):
    """Controller that figures out settings and renders file structure.

    :param template: Template name
    :param target_directory: Filesystem path to a output directory
    :param bobconfig: Configuration for mr.bob behaviour
    :param variables: Given variables

    TODO: describe what configurator does
    TODO: display api variables

    """

    def __init__(self,
                 template,
                 target_directory,
                 bobconfig=None,
                 variables=None):
        if not bobconfig:
            bobconfig = {}
        if not variables:
            variables = {}
        self.variables = variables
        self.target_directory = os.path.realpath(target_directory)
        if not os.path.isdir(self.target_directory):
            os.makedirs(self.target_directory)

        # figure out template directory
        self.template_dir, self.is_tempdir = parse_template(template)

        # parse template configuration file
        template_config = os.path.join(self.template_dir, '.mrbob.ini')
        if not os.path.exists(template_config):
            raise TemplateConfigurationError('Config not found: %s' % template_config)
        self.config = parse_config(template_config)

        # parse questions from template configuration file
        self.raw_questions = self.config['questions']
        if self.raw_questions:
            self.questions = self.parse_questions(self.raw_questions, self.config['questions_order'])
        else:
            self.questions = []

        # parse bobconfig settings
        # TODO: move config resolution inside this function from cli.py
        self.bobconfig = update_config(bobconfig, self.config['mr.bob'])
        self.renderer = resolve_dotted_func(
            self.bobconfig.get('renderer', 'mrbob.rendering:jinja2_renderer'))
        self.verbose = self.bobconfig.get('verbose', False)
        self.post_render_msg = self.bobconfig.get('post_render_msg', '')
        self.preserve_mrbob_config = self.bobconfig.get('preserve_mrbob_config', False)
        self.post_render = [resolve_dotted_func(f) for f in self.bobconfig.get('post_render', '').split()]
        self.pre_render = [resolve_dotted_func(f) for f in self.bobconfig.get('pre_render', '').split()]
        self.pre_ask_question = [resolve_dotted_func(f) for f in self.bobconfig.get('pre_ask_question', '').split()]
        self.post_ask_question = [resolve_dotted_func(f) for f in self.bobconfig.get('post_ask_question', '').split()]

    def render(self):
        """Render file structure given instance configuration. Basically calls
        :func:`mrbob.rendering.render_structure`.
        """
        if self.pre_render:
            for f in self.pre_render:
                f(self)
        render_structure(self.template_dir,
                         self.target_directory,
                         self.variables,
                         self.verbose,
                         self.renderer,
                         self.preserve_mrbob_config)
        if self.post_render:
            for f in self.post_render:
                f(self)
        if self.post_render_msg:
            print self.post_render_msg % self.variables

    def parse_questions(self, config, order):
        q = []

        for question_key in order:
            key_parts = question_key.split('.')
            c = dict(config)
            for k in key_parts:
                c = c[k]
            # filter out subnamespaces
            c = dict([(k, v) for k, v in c.items() if not isinstance(v, dict)])
            try:
                question = Question(name=question_key, **c)
            except TypeError:
                raise TemplateConfigurationError(
                    'Question "%s" got an unexpected argument. Arguments: %s' % (question_key, ', '.join(c)))

            q.append(question)
        return q

    def print_questions(self):  # pragma: no cover
        for line in pretty_format_config(self.raw_questions):
            print(line)
            # TODO: filter out lines without questions
            # TODO: seperate questions with a newline
            # TODO: keep order

    def ask_questions(self):
        """Loops through questions and asks for input if variable is not yet set.
        """
        # TODO: deepcopy + while loop + pop
        for question in self.questions:
            if self.pre_ask_question:
                for f in self.pre_ask_question:
                    f(question, self)
            if question.name in self.variables:
                pass  # TODO: pass to ask method to validate input?
            else:
                answer = question.ask()
                self.variables[question.name] = answer
            if self.post_ask_question:
                for f in self.post_ask_question:
                    f(question, self)


class Question(object):
    """Question configuration. Parameters are used to configure validation of the answer.
    """

    def __init__(self,
                 name,
                 question,
                 default=None,
                 required=False,
                 action=lambda x: x,
                 validator=None,
                 command_prompt=six.moves.input,
                 help=""):
        self.name = name
        self.question = question
        self.default = default
        self.required = maybe_bool(required)
        if maybe_bool(self.default) and self.required:
            raise TemplateConfigurationError('Question %s is required but has also defined a default.' % self.name)
        self.validator = maybe_resolve_dotted_func(validator)
        self.action = maybe_resolve_dotted_func(action)
        self.command_prompt = maybe_resolve_dotted_func(command_prompt)
        self.help = help
        # TODO: provide basic validators
        # TODO: choice question?

    def __repr__(self):
        return six.u("<Question name=%(name)s question='%(question)s' default=%(default)s required=%(required)s>") % self.__dict__

    def ask(self):
        """Eventually, ask the question.
        """
        correct_answer = None

        try:
            while correct_answer is None:
                if self.default:
                    question = six.u("--> %s [%s]: ") % (self.question, self.default)
                else:
                    question = six.u("--> %s: ") % self.question
                if six.PY3:  # pragma: no cover
                    answer = self.command_prompt(question).strip()
                else:  # pragma: no cover
                    answer = self.command_prompt(question.encode('utf-8')).strip().decode('utf-8')
                if answer == "?":
                    if self.help:
                        print(self.help)
                    else:
                        print("There is no additional help text.")
                    continue

                if self.validator and answer:
                    try:
                        _ = self.validator(answer)
                        if _:
                            answer = _
                    except ValidationError as e:
                        print('    Error:' + str(e))
                        continue

                if answer:
                    correct_answer = answer
                elif not answer and self.default is not None:
                    correct_answer = maybe_bool(self.default)
                elif not answer and self.default is None:
                    if self.required:
                        continue
                    else:
                        correct_answer = answer
        except KeyboardInterrupt:  # pragma: no cover
            print('\nExiting...')
            sys.exit(0)

        print('')
        return self.action(correct_answer)
