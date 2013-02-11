# -*- coding: utf-8 -*-

import os
import textwrap
import sys

import parsing


class Attributes(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def register_template(template_rel_dir, description=""):
    """Register a project template

    :param template_rel_dir: relative path to the template root (contains .mrbob.ini)
    :param description: a full text description of the project template
    """
    caller_file = sys._getframe(1).f_globals['__file__']  # The module that called register_template
    template_dir = os.path.join(os.path.dirname(caller_file), template_rel_dir)
    if not os.path.isdir(template_dir):
        raise ValueError("{0} is not a directory".format(template_dir))
    mrbob_ini_path = os.path.join(template_dir, '.mrbob.ini')
    if not os.path.isfile(mrbob_ini_path):
        raise ValueError("{0} is not a mr.bob template (has no .mrbob.ini file)".format(template_dir))

    if len(description) == 0:
        # Try to get description from .mrbob.ini
        config = parsing.parse_config(mrbob_ini_path)
        description = config.get('template', {}).get('description')
        if description is None:
            description = "No description available"
    indent = '    '
    description = textwrap.fill(description.strip(), width=79, initial_indent=indent,
                                subsequent_indent=indent)
    return Attributes(directory=template_dir, description=description)
