""""""

import os
from importlib import import_module

from .rendering import render_structure


class ConfigurationError(Exception):
    """Raised during configuration phase"""


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
        # TODO: get variables from template_dir/questions.ini
        self.variables = {}
        self.target_directory = os.path.realpath(target_directory)
        if not os.path.isdir(self.target_directory):
            os.makedirs(self.target_directory)
        self.bobconfig = bobconfig
        self.renderer = resolve_dotted_func(bobconfig['renderer'])

    def get_questions(self):  # pragma: no cover
        # TODO: return information about questions
        return

    def render(self):
        render_structure(self.template_dir,
                         self.target_directory,
                         self.variables,
                         self.renderer)
