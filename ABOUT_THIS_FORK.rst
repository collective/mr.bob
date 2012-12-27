===============
About this fork
===============

This is a fork of the original `mr.bob <https://github.com/iElectric/mr.bob>`_
that adds the following features :

setuptools style templates registration and discovery
=====================================================

Packages with templates for `mr.bob`_ can register setuptools entry points in
the ``setup.py`` ``setup(...)`` function::

  setup(
      ...
      entry_points={
          'mrbobtemplates': [
              'mrbobname=mrbobtemplates.mytemplates:localname
          ]
      },
      ...
  )

Where :

``mrbobtemplates``
  The key used to register templates for mr.bob.

``mrbobname``
   The name of the template as registered for mr.bob. All available names and
   respective templates descriptions are displayed with the command ``mrbob
   --list-templates``.

``mrbobtemplate.mytemplates``
  The module that defines the template descriptor object. Typically the main
  ``__init__.py`` of your package.

``localname``
  A dict with two keys:

  - ``directory``: the absolute path of the regular mr.bob template (that
    contains the ``.mrbob.ini`` file).
  - ``description``: some lines of text that describe what you template
    provides.

Given such this package structure::

  - (root with "setup.py"...)
  |- mrbobtemplates/
     |- mytemplates/
        |- __init__.py
        |- localname/ (a template directory with ".mrbob.ini")

You should have something like this in the ``__init__.py`` ::

  import os
  ...
  this_directory = os.path.dirname(os.path.abspath(__file__))
  localname = {
      'directory': os.path.join(this_directory, 'localname'),
      'description': "A very nice personal template. Lorem ipsum..."
  }

As viewed above, ``mrbob`` command comes with the following new options:

- ``--list-templates``: show the registered templates and exits.
- ``--template / -t TEMPLATE``: use the registered template named TEMPLATE.

As a consequence, given the above example and existing ``mrbob`` command, the
following commands are equivalent ::

  $ mrbob -t localname -O my.project
  $ mrbob -O my.project mrbobtemplates.mytemplates:localname

Python computed additional variables
====================================

Building additional variables in the JinJa2 templates is not an easy
thing. Playing with Python code is easier to add some things like the current
year or mangling other variables coming from ``.mrbob.ini`` processing.

This branch enables template authors to provide a ``.mrbob.py`` script, located
in the root of the template structure, beside ``.mrbob.ini``.

This script is executed after the relies to the questions stated in
``.mrbob.ini``. The variables coming from this questions processing are pushed
in the namespace of ``.mrbob.py``.

The variables from the global namespace of this script are available to the
templates in addition to the ones that come from the execution of the wizard.

Example
=======

The above described new features are leveraged in the package
`mrbobtemplates.gillux <https://github.com/glenfant/mrbobtemplates.gillux>`_.
