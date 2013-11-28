#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Doc here.
"""

__docformat__ = 'restructuredtext en'


class FooRenderFilename():
    order = 15

    def __init__(self, filename, variables):
        self.filename = filename
        self.variables = variables

    def get_filename(self):
        return 'fake_foo_' + self.filename, True


class BarRenderFilename():
    order = 20

    def __init__(self, filename, variables):
        self.filename = filename
        self.variables = variables

    def get_filename(self):
        return self.filename + '_fake_bar', False


class BadRenderFilename():
    """A bad plugin which has not get_filename method."""


# vim:set et sts=4 ts=4 tw=80:
