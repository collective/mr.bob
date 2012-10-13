""""""

import os
from importlib import import_module

from .rendering import render_structure


def resolve_dotted(name):
    module_name, dir_name = name.split(':')
    module = import_module(module_name)
    return os.path.join(os.path.dirname(module.__file__), dir_name)


def parse_template(template_name):
    if ':' in template_name:
        path = resolve_dotted(template_name)
    else:
        path = os.path.realpath(template_name)

    if not os.path.isdir(path):
        raise ValueError('Template directory does not exist: %s' % path)
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
        self.renderer = import_module(bobconfig.get('renderer',
            'mrbob.rendering.python_formatting_renderer'))

    def get_questions(self):  # pragma: no cover
        # TODO: return information about questions
        return

    def render(self):
        render_structure(self.template_dir,
                         self.target_directory,
                         self.variables,
                         self.renderer)
