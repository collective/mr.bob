""""""

import os
import re
import sys
import readline
readline  # make pyflakes happy, readline makes interactive mode keep history

import six
from importlib import import_module

from .rendering import render_structure
from .parsing import parse_config, pretty_format_config


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
    module_name, dir_name = name.split(':')
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
    if value in ('True', 'False'):
        return bool(value)
    else:
        return value


def parse_template(template_name):
    if ':' in template_name:
        path = resolve_dotted_path(template_name)
    else:
        path = os.path.realpath(template_name)

    if not os.path.isdir(path):
        raise ConfigurationError('Template directory does not exist: %s' % path)
    return path


class Configurator(object):
    """"""

    def __init__(self,
                 template,
                 target_directory,
                 bobconfig):
        self.template_dir = parse_template(template)
        template_config = os.path.join(self.template_dir, '.mrbob.ini')
        if not os.path.exists(template_config):
            raise TemplateConfigurationError('Config not found: %s' % template_config)
        self.raw_questions = parse_config(template_config)['questions']
        # TODO: first aggregate all config, then generate questions
        self.questions = self.parse_questions(self.raw_questions)
        self.target_directory = os.path.realpath(target_directory)
        if not os.path.isdir(self.target_directory):
            os.makedirs(self.target_directory)
        self.bobconfig = bobconfig
        self.renderer = resolve_dotted_func(
            bobconfig.get('renderer', 'mrbob.rendering:jinja2_renderer'))
        self.verbose = bobconfig.get('verbose', False)
        self.variables = {}

    def render(self):
        render_structure(self.template_dir,
                         self.target_directory,
                         self.variables,
                         self.renderer)

    def parse_questions(self, config):
        q = []
        for line in pretty_format_config(config):
            key, value = line.split(' = ')
            key_parts = key.split('.')
            if key_parts[-1] == 'question':
                c = dict(config)
                for k in key_parts[:-1]:
                    c = c[k]
                # filter out subnamespaces
                c = dict([(k, value) for k, value in c.items() if not isinstance(value, dict)])
                name = '.'.join(key_parts[:-1])
                try:
                    question = Question(name=name, **c)
                except TypeError:
                    raise TemplateConfigurationError(
                        'Question "%s" got an unexpected argument. Arguments: %s' % (name, ', '.join(c)))

                q.append(question)
        return q

    def print_questions(self):  # pragma: no cover
        for line in pretty_format_config(self.raw_questions):
            print(line)
            # TODO: filter out lines without questions
            # TODO: seperate questions with a newline


class Question(object):
    """"""

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
        self.default = maybe_bool(default)
        # TODO: if we have default, then it shouldn't be required
        self.required = maybe_bool(required)
        self.validator = maybe_resolve_dotted_func(validator)
        self.action = maybe_resolve_dotted_func(action)
        self.command_prompt = maybe_resolve_dotted_func(command_prompt)
        self.help = help
        # TODO: provide basic validators
        # TODO: choice question?

    def __repr__(self):
        return six.u("<Question name=%(name)s question='%(question)s' default=%(default)s required=%(required)s>") % self.__dict__

    def ask(self):
        correct_answer = None

        try:
            while correct_answer is None:
                if self.default:
                    question = "--> " + self.question + " [" + self.default + "]:"
                else:
                    question = "--> " + self.question + ":"
                answer = self.command_prompt(question).strip()
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
                    correct_answer = self.default
                elif not answer and self.default is None:
                    continue
        except KeyboardInterrupt:  # pragma: no cover
            print('Exiting...')
            sys.exit(0)

        return self.action(correct_answer)
