.. highlight:: bash


User guide
==========

Installation
------------

::

    $ pip install mr.bob


Usage
-----


Once you install mr.bob, there is `mrbob` command available::

    $ mrbob --help
    usage: mrbob [-h] [-O TARGET_DIRECTORY] [-c CONFIG] [-V] [-l] [-r RENDERER]
                 [template]

    Filesystem template renderer

    positional arguments:
      template              Template to use for rendering

    optional arguments:
      -h, --help            show this help message and exit
      -O TARGET_DIRECTORY, --target-directory TARGET_DIRECTORY
                            Where to output rendered structure. Defaults to
                            current directory.
      -c CONFIG, --config CONFIG
                            Configuration file to specify either [mr.bob] or
                            [variables] sections.
      -V, --version         Display version number
      -l, --list-questions  List all questions needed for the template
      -r RENDERER, --renderer RENDERER
                            Dotted notation to a renderer function. Defaults to
                            mrbob.rendering:jinja2_renderer

Most basic use case is rendering a template from a folder to current folder::

    $ mrbob template_folder/

Or from a package::

    $ mrbob some.package:template_folder/

    some.python.package:relative/path/to/template\n
    relative/path/to/template\n
    /absolute/path/to/template
    https://github.com/iElectric/mr.bob/zipball/master
    https://github.com/iElectric/mr.bob/zipball/master#relative/path/to/template


Sample template to try out
--------------------------

::

    $ mrbob mr.bob.templates:sample/
    ... TODO: write this


Listing all questions needed to have corresponding variable for a template
--------------------------------------------------------------------------

::

    $ mrbob --list-questions mr.bob.templates:sample/
    ... TODO: write this


Configuration
-------------

Configuration is done with `.ini` style files. There are two sections for configuration.

mr.bob
    configures how `mrbob` behaves
variables
    answers to the questions that will be passed to templates for rendering

Example of global config file `~/.mrbob` or command line parameter `mrbob --config foo.ini`.

.. code-block:: ini

    [mr.bob]
    renderer = moo.foo:render_mako

    [variables]
    author = Domen Kožar
    author.email = domen@dev.si


Configuration inheritance
*************************

Configuration can be specified in multiple ways. Here is a graph how settings are preferred (questions override any other configuration).
::

    Global config at ~/.mrbob
            ^
            |
    mrbob --config mrbob.ini
            ^
            |
    Questions answered in interactive mode


Nesting variables into namespaces called groups
***********************************************

All variables can be specified in namespaces, such as `author.name`. Currently namespaces
don't do anything special besides providing readability.



``mr.bob`` section reference
****************************

============  ===============================  ===============================================================
  Parameter      Default                          Explanation
============  ===============================  ===============================================================
  renderer    mrbob.rendering:jinja2_renderer  Function for rendering templates
  verbose     False                            Output more information, useful for debugging
============  ===============================  ===============================================================



Collection of community managed templates
-----------------------------------------

You are encouraged to use `bobtemplates.something` Python egg namespace to write
templates and contribute them to this list by making a `pull request <github.com/iElectric/mr.bob>`_.

- `bobtemplates.ielectric <https://github.com/iElectric/bobtemplates.ielectric>`_ 
