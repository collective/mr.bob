Welcome to mr.bob's documentation!
==================================

:Author: Tom Lazar <tom@tomster.org>, Domen Kožar <domen@dev.si>
:Source code: `github.com project <https://github.com/iElectric/mr.bob>`_
:Bug tracker: `github.com issues <https://github.com/iElectric/mr.bob/issues>`_
:License: BSD
:Generated: |today|
:Version: |release|


.. sidebar:: Features

    - provide questions needed to be answered for rendering structure
    - questions can be grouped by using a namespace
    - render templates from a folder or Python egg or zip file
    - supports Python 2.6 - 3.3, pypy
    - 100% test coverage
    - uses Jinja2 as default rendering engine (can be replaced)
    - multiple ways to specify variables to render templates
    - preserves permissions when rendering templates

   **Flow of mr.bob** 

   .. import mr.bob_flow.xml to diagram.ly to export image as .jpg
   .. image:: mr.bob_flow.jpg


.. topic:: Introduction

   **mr.bob** is a tool that takes a directory skeleton and copies over
   directory structure to target folder and might use rendering engine
   `Jinja2 <http://jinja.pocoo.org/>`_ to dynamically generate the files. Additionally, you might be
   asked some questions needed to render the structure or provide a config
   file to answer them.

   **mr.bob** is meant to deprecate previous tools such as
   `paster (PasteScript) <http://pythonpaste.org/script/>`_
   and `templer <http://templer-manual.readthedocs.org/en/latest/index.html>`_.


.. toctree::
   :maxdepth: 3

   userguide.rst
   templateauthor.rst
   other.rst
   developer.rst
   api.rst


Glossary
========

dotted notation
   Importable Python function specified with dots as importing a module separated with a column
   to denote a function. For example *mrbob.rendering:render_structure*
mr.bob
    configures how `mrbob` behaves
variables
    answers to the questions that will be passed to templates for rendering


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

