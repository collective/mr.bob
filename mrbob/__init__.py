# -*- coding: utf-8 -*-

import os
import abc
import textwrap

import parsing


class TemplateDescription(object):
    """Base class for templates registered through setuptools entry_points
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def path(self):
        """Absolute path to the template (folder that contains.mrbob.ini)
        This property **must** be overriden by subclasses
        """
        return '/home/me/mytemplate'

    @property
    def description(self):
        """Provides an unformatted description with useful end-user information.
        By default, we shall provide the text that's in "description" option of
        the "template" section of file .mrbob.ini
        Anyway, authors of mrbob templates may override it
        """
        config = parsing.parse_config(os.path.join(self.path, '.mrbob.ini'))
        description = config.get('template', {}).get('description')
        if description is not None:
            return description
        else:
            return "No description available"

    @property
    def formatted_description(self):
        """An UI suited description
        """
        indent = '    '
        return textwrap.fill(self.description.strip(), width=79, initial_indent=indent,
                             subsequent_indent=indent)
