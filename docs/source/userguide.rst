.. highlight:: bash


User guide
==========

Installation
------------

::

    pip install mr.bob


Usage
-----


Once you install mr.bob, there is `mrbob` command available::

    $ mrbob --help
    usage: mrbob [-h] [-O, --target-directory TARGET_DIRECTORY] [--verbose]
                 [--version] [--list-questions]
                 [template]

    Filesystem template renderer

    positional arguments:
      template              Template to use for rendering

    optional arguments:
      -h, --help            show this help message and exit
      -O, --target-directory TARGET_DIRECTORY
                            Where to output rendered structure
      --verbose             Print more output for debugging
      --version             Display version number
      --list-questions      List all questions needed for the template

Most basic use case is rendering a template from a folder to current folder::

    $ mrbob template_folder/

Or from a package::

    $ mrbob some.package:template_folder/


Using a sample template
-----------------------


    $ mrbob mr.bob.templates:sample/
    ...


Configuration
-------------

Configuration is done with `.ini` style files. There are two sections for configuration.

mr.bob
    configures how `mrbob` behaves
variables
    parameters that will be passed to templates for rendering

Configuration can be specified in multiple ways. Here is a graph how settings are preferred (questions override any other configuration).

::

    Global config at ~/.mrbob
        ^
        |
    mrbob --config mrbob.ini
        ^
        |
    mrbob --some-variable foobar
        ^
        |
    questions answered in interactive mode


Example of global config file `~/.mrbob` or command line parameter `mrbob --config foo-ini`.

.. code-block:: ini

    [mr.bob]
    non-interactive = true
    renderer = moo.foo:render_mako

    [variables]
    author = Domen Kožar
    author_email = domen@dev.si
    foo.bar = something


TODO: explain grouped variables

Listing all questions needed to be answered for a template
----------------------------------------------------------

::

    $ mrbob --list-questions template_folder/
    ...


Collection of community managed templates
-----------------------------------------

You are encouraged to use `bobtemplates.*` Python egg namespace to write
templates and contribute them to this list by making a pull request.

- `bobtemplates.ielectric <https://github.com/iElectric/bobtemplates.ielectric>`_ 


Design goals
------------

- Cover 80% of use cases, don't become too complex  
- Ability to use templates not only from eggs, but also folders and similar
- Python 3 support
- Jinja2 renderer by default, but replaceable
- Ability to render multiple templates to the same target directory
