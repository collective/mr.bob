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
readline  # NOQA: make pyflakes happy, readline makes interactive mode keep history

import six
from importlib import import_module

from .rendering import render_structure
from .parsing import (
    parse_config,
    write_config,
    update_config,
    pretty_format_config,
)
from .bobexceptions import (
    ConfigurationError,
    TemplateConfigurationError,
    SkipQuestion,
    ValidationError,
)


DOTTED_REGEX = re.compile(r'^[a-zA-Z_.]+:[a-zA-Z_.]+$')


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
        raise ConfigurationError("There is no object named %s in module %s" % (func_name, module_name))


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
            urlretrieve(url, tmpfile.name)
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
    """Controller that figures out settings, asks questions and renders
    the directory structure.

    :param template: Template name
    :param target_directory: Filesystem path to a output directory
    :param bobconfig: Configuration for mr.bob behaviour
    :param variables: Given variables to questions
    :param defaults: Overriden defaults of the questions

    Additional to above settings, `Configurator` exposes following attributes:

    - :attr:`template_dir` is root directory of the template
    - :attr:`is_tempdir` if template directory is temporary (when using zipfile)
    - :attr:`templateconfig` dictionary parsed from `template` section
    - :attr:`questions` ordered list of `Question instances to be asked
    - :attr:`bobconfig` dictionary parsed from `mrbob` section of the config

    """

    def __init__(self,
                 template,
                 target_directory,
                 bobconfig=None,
                 variables=None,
                 defaults=None):
        if not bobconfig:
            bobconfig = {}
        if not variables:
            variables = {}
        if not defaults:
            defaults = {}
        self.variables = variables
        self.defaults = defaults
        self.target_directory = os.path.realpath(target_directory)

        # figure out template directory
        self.template_dir, self.is_tempdir = parse_template(template)

        # check if user is trying to specify output dir into template dir
        if self.template_dir in os.path.commonprefix([self.target_directory,
                                                      self.template_dir]):
            raise ConfigurationError('You can not use target directory inside the template')

        if not os.path.isdir(self.target_directory):
            os.makedirs(self.target_directory)

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
        self.verbose = maybe_bool(self.bobconfig.get('verbose', False))
        self.quiet = maybe_bool(self.bobconfig.get('quiet', False))
        self.remember_answers = maybe_bool(self.bobconfig.get('remember_answers', False))
        self.ignored_files = self.bobconfig.get('ignored_files', '').split()
        self.ignored_directories = self.bobconfig.get('ignored_directories', '').split()

        # parse template settings
        self.templateconfig = self.config['template']
        self.post_render = [resolve_dotted_func(f) for f in self.templateconfig.get('post_render', '').split()]
        self.pre_render = [resolve_dotted_func(f) for f in self.templateconfig.get('pre_render', '').split()]
        self.post_ask = [resolve_dotted_func(f) for f in self.templateconfig.get('post_ask', '').split()]
        self.pre_ask = [resolve_dotted_func(f) for f in self.templateconfig.get('pre_ask', '').split()]
        self.renderer = resolve_dotted_func(
            self.templateconfig.get('renderer', 'mrbob.rendering:jinja2_renderer'))

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
                         self.ignored_files,
                         self.ignored_directories)
        if self.remember_answers:
            write_config(os.path.join(self.target_directory, '.mrbob.ini'),
                         'variables',
                         self.variables)
        if self.post_render:
            for f in self.post_render:
                f(self)

    def parse_questions(self, config, order):
        q = []

        for question_key in order:
            key_parts = question_key.split('.')
            c = dict(config)
            for k in key_parts:
                c = c[k]
            # filter out subnamespaces
            c = dict([(k, v) for k, v in c.items() if not isinstance(v, dict)])
            question = Question(name=question_key, **c)
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
        if self.pre_ask:
            for f in self.pre_ask:
                f(self)
        # TODO: if users want to manipulate questions order, this is curently not possible.
        for question in self.questions:
            if question.name not in self.variables:
                self.variables[question.name] = question.ask(self)
        if self.post_ask:
            for f in self.post_ask:
                f(self)


class Question(object):
    """Question configuration. Parameters are used to configure questioning
    and possible validation of the answer.

    :param name: Unique, namespaced name of the question
    :param question: Question to be asked
    :param default: Default value of the question
    :param required: Is question required?
    :type required: bool
    :param command_prompt: Function to executed to ask the question given question text
    :param help: Optional help message
    :param pre_ask_question: Space limited functions in dotted notation to ask before the question is asked
    :param post_ask_question: Space limited functions in dotted notation to ask aster the question is asked
    :param **extra: Any extra parameters stored for possible extending of `Question` functionality

    Any of above parameters can be accessed as an attribute of `Question` instance.

    """

    def __init__(self,
                 name,
                 question,
                 default=None,
                 required=False,
                 command_prompt=six.moves.input,
                 pre_ask_question='',
                 post_ask_question='',
                 help="",
                 **extra):
        self.name = name
        self.question = question
        self.default = default
        self.required = maybe_bool(required)
        self.command_prompt = maybe_resolve_dotted_func(command_prompt)
        self.help = help
        self.pre_ask_question = [resolve_dotted_func(f) for f in pre_ask_question.split()]
        self.post_ask_question = [resolve_dotted_func(f) for f in post_ask_question.split()]
        self.extra = extra

    def __repr__(self):
        return six.u("<Question name=%(name)s question='%(question)s'"
                     " default=%(default)s required=%(required)s>") % self.__dict__

    def ask(self, configurator):
        """Eventually, ask the question.

        :param configurator: :class:`mrbob.configurator.Configurator` instance

        """
        correct_answer = None
        self.default = configurator.defaults.get(self.name, self.default)
        non_interactive = maybe_bool(configurator.bobconfig.get('non_interactive', False))
        if non_interactive:
            self.command_prompt = lambda x: ''

        try:
            while correct_answer is None:
                # hook: pre ask question
                for f in self.pre_ask_question:
                    try:
                        f(configurator, self)
                    except SkipQuestion:
                        return

                # prepare question
                if self.default:
                    question = six.u("--> %s [%s]: ") % (self.question, self.default)
                else:
                    question = six.u("--> %s: ") % self.question

                # ask question
                if six.PY3:  # pragma: no cover
                    answer = self.command_prompt(question).strip()
                else:  # pragma: no cover
                    answer = self.command_prompt(question.encode('utf-8')).strip().decode('utf-8')

                # display additional help
                if answer == "?":
                    if self.help:
                        print(self.help)
                    else:
                        print("There is no additional help text.")
                    continue

                if answer:
                    correct_answer = answer
                # if we don't have an answer, take default
                elif self.default is not None:
                    correct_answer = maybe_bool(self.default)
                # if we don't have an answer or default value and is required, reask
                elif self.required and not correct_answer:
                    if non_interactive:
                        raise ConfigurationError('non-interactive mode: question %s is required but not answered.' % self.name)
                    else:
                        # TODO: we don't cover this as coverage seems to ignore it
                        continue  # pragma: no cover
                else:
                    correct_answer = answer

                # hook: post ask question + validation
                for f in self.post_ask_question:
                    try:
                        correct_answer = f(configurator, self, correct_answer)
                    except ValidationError as e:
                        if non_interactive:
                            raise ConfigurationError('non-interactive mode: question %s failed validation.' % self.name)
                        else:
                            correct_answer = None
                            print("ERROR: " + str(e))
                            continue
        except KeyboardInterrupt:  # pragma: no cover
            print('\nExiting...')
            sys.exit(0)

        if not non_interactive:
            print('')
        return correct_answer
