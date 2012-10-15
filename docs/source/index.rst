Welcome to mr.bob's documentation!
==================================

:Author: Tom Lazar <tom@tomster.org>, Domen Kožar <domen@dev.si>
:Source code: `github.com project <https://github.com/iElectric/mr.bob>`_
:Bug tracker: `github.com issues <https://github.com/iElectric/mr.bob/issues>`_
:License: BSD
:Generated: |today|
:Version: |release|


.. sidebar:: Features

    - provide questions needed to be answered
    - questions can be grouped by using a namespace
    - render templates from a folder or Python egg
    - supports Python 2.6 - 3.3, pypy
    - 100% test coverage
    - uses Jinja2 as default rendering engine (can be replaced)
    - preserves permissions when rendering templates


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
   developer.rst
   api.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

