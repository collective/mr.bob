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
              'mrbobname=mrbobtemplates.mytemplates:templateobj
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

``templateobj``

  Your template registration. This object sits typically in the __init__.py of
  your template package. The ``templateobj`` is created by the factory function
  ``mrbob.register_template``

Given such this package structure::

  - (root with "setup.py"...)
  |- mrbobtemplates/
     |- mytemplates/
        |- __init__.py
        |- a_template/ (a template directory with ".mrbob.ini")

You should have something like this in the ``__init__.py`` ::

  from mrbob import register_template

  # ``templateobj`` being the last name of your registration in ``setup.py``
  templateobj = register_template('a_template')

And in ``mrbobtemplates/mytemplates/a_template/.mrbob.ini``::

  [template]
  description = A bootstrap for a WSGI middleware with tests

Another option to provide a description of your template is to provide the
optional ``description`` parameter to the ``register_template`` factory
function ::

  templateobj = register_template('a_template', description="A fancy project bootstrap")

Using a template
----------------

Is just like in previous versions of ``mr.bob``. But the template is searched
in the registered names before looking into the filesystem.


Example
=======

The above described new features are leveraged in the package
`mrbobtemplates.gillux <https://github.com/glenfant/mrbobtemplates.gillux>`_.
