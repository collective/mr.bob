Welcome to mr.bob's documentation!
==================================

:Author: Tom Lazar <tom@tomster.org>, Domen Kožar <domen@dev.si>
:Source code: `github.com project <https://github.com/iElectric/mr.bob>`_
:Bug tracker: `github.com issues <https://github.com/iElectric/mr.bob/issues>`_
:License: BSD
:Generated: |today|
:Version: |release|


.. sidebar:: Features

    - asks questions which need to be answered to render structure
    - questions can be grouped by using a namespace
    - renders templates from a folder, Python egg, or zip file
    - supports Python 2.6 - 3.3, pypy
    - 100% test coverage
    - uses Jinja2 as the default rendering engine (can be replaced)
    - multiple ways to specify variables to render templates
    - preserves permissions when rendering templates
    - provides hooks before/after asking a question
    - provides hooks before/after rendering structure
    - can remember given answers for rendered structure

   **Flow of mr.bob** 

   .. import mr.bob_flow.xml to diagram.ly to export image as .jpg
   .. image:: mr.bob_flow.jpg


.. topic:: Introduction

   **mr.bob** is a tool that takes a directory skeleton, copies over
   its directory structure to a target folder and can use the `Jinja2
   <http://jinja.pocoo.org/>`_ (or some other) templating engine to dynamically
   generate the files. Additionally, it can ask you questions needed
   to render the structure, or provide a config file to answer them.

   **mr.bob** is meant to deprecate previous tools such as
   `paster (PasteScript) <http://pythonpaste.org/script/>`_
   and `templer <http://templer-manual.readthedocs.org/en/latest/index.html>`_.


.. toctree::
   :maxdepth: 3

   userguide.rst
   templateauthor.rst
   pluginauthor.rst
   other.rst
   developer.rst
   api.rst
   HISTORY.rst


Glossary
========

.. glossary::

   dotted notation
      Importable Python function specified with dots as importing a module separated with a column
      to denote a function. For example *mrbob.rendering:render_structure*

   mr.bob
      This section configures how `mrbob` behaves

   variables
      This section answers to the questions that will be passed to templates for rendering


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

