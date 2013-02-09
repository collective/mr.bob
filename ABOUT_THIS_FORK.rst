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
          'bobtemplates': [
              'mrbobname=mrbobtemplates.mytemplates:TemplateClass
          ]
      },
      ...
  )

Where :

``bobtemplates``
  The key used to register templates for mr.bob.

``mrbobname``
   The name of the template as registered for mr.bob. All available names and
   respective templates descriptions are displayed with the command ``mrbob
   --list-templates``.

``mrbobtemplate.mytemplates``
  The module that defines the template description class. Typically the main
  ``__init__.py`` of your package.


``TemplateClass``
  A class, in the ``__init__.py`` of the template package, that describes the
  template, preferably inheriting from ``mrbob.TemplateDescription``. This
  class must provide a ``path`` attribute that is the absolute path of a
  template (that contains a ``.mrbob.ini`` file). This class may have a
  ``description`` property that provides a plain text description of the
  template for the end user. This description shows up when using the
  ``--list-templates`` option. If the class does not provide a
  ``description``, we use the ``description`` option of the ``[template]``
  section of ``.mrbob.ini``.

Given such this package structure::

  - (root with "setup.py"...)
  |- mrbobtemplates/
     |- mytemplates/
        |- __init__.py
        |- a_template/ (a template directory with ".mrbob.ini")

You should have something like this in the ``__init__.py`` ::

  import os
  import mrbob
  ...
  this_directory = os.path.dirname(os.path.abspath(__file__))

  class MyTemplateClass(mrbob.TemplateDescription):
      path = os.path.join(this_directory, 'a_template')  # contains .mrbob.ini

And in ``mrbobtemplates/mytemplates/a_template/.mrbob.ini``::

  [template]
  description = A bootstrap for a WSGI middleware with tests

Using a template
----------------

Is just like in previous versions of ``mr.bob``. But the template is searched
in the registered names before looking into the filesystem.


Example
=======

The above described new features are leveraged in the package
`mrbobtemplates.gillux <https://github.com/glenfant/mrbobtemplates.gillux>`_.
