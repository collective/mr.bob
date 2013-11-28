.. highlight:: bash


User guide
==========

Installation
------------

::

    $ pip install mr.bob


Usage
-----


Once you install mr.bob, the ``mrbob`` command is available::

    $ mrbob --help
    usage: mrbob [-h] [-O TARGET_DIRECTORY] [-v] [-c CONFIG] [-V] [-l] [-w] [-n]
                 [-q]
                 [template]

    Filesystem template renderer

    positional arguments:
      template              Template name to use for rendering. See http://mrbob.r
                            eadthedocs.org/en/latest/userguide.html#usage for a
                            guide to template syntax

    optional arguments:
      -h, --help            show this help message and exit
      -O TARGET_DIRECTORY, --target-directory TARGET_DIRECTORY
                            Where to output rendered structure. Defaults to
                            current directory
      -v, --verbose         Print more output for debugging
      -c CONFIG, --config CONFIG
                            Configuration file to specify either [mr.bob] or
                            [variables] sections
      -V, --version         Display version number
      -l, --list-questions  List all questions needed for the template
      -w, --remember-answers
                            Remember answers to .mrbob.ini file inside output
                            directory
      -n, --non-interactive
                            Don't prompt for input. Fail if questions are required
                            but not answered
      -q, --quiet           Suppress all but necessary output
      -r RDR_FNAME_PLUGIN_TARGET, --rdr-fname-plugin-target RDR_FNAME_PLUGIN_TARGET
                            Specify target plugin like 10|20

By default, the target directory is the current folder. The most basic use case is rendering a template from a relative folder::

    $ mrbob ../template_folder/

Or from a package::

    $ mrbob some.package:template_folder/

Or from a zip file::

    $ mrbob https://github.com/iElectric/mr.bob/zipball/master

Or from a relative path in a zip file::

    $ mrbob https://github.com/iElectric/mr.bob/zipball/master#mrbob/template_sample


Sample template to try out
--------------------------

::

    $ mrbob mrbob:template_sample/
    Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Value in square brackets at the end of the questions present default value if there is no answer.


    --> How old are you? [24]: 

    --> What is your name?: Foobar

    --> Enter password: 


    Generated file structure at /current/directory/


Listing all questions needed to have corresponding variable for a template
--------------------------------------------------------------------------

::

    $ mrbob --list-questions mrbob:template_sample/
    author.age.default = 24
    author.age.help = We need your age information to render the template
    author.age.question = How old are you?
    author.name.question = What is your name?
    author.name.required = True
    author.password.command_prompt = getpass:getpass
    author.password.question = Enter password


Remember answers to a config file
------------------------------------

Running::

    $ mrbob --remember-answers -O new_dir mrbob:template_sample/
    ...

When everything is done, all answers are stored in **new_dir/.mrbob.ini**
so later you reuse them::

    $ mrbob --config new_dir/.mrbob.ini -O new_dir another_template/
    ...


Using ``non-interactive`` mode
--------------------------------

Sometimes you might want to automate a script and use ``mrbob``. It
is wise to tell ``mrbob`` to not prompt for any input. ``mrbob`` will use
given answers and defaults if answers are missing. In case a question
is required and doesn't have a default, error will be thrown.

Configuration
-------------

Configuration is done with ``.ini`` style files. There are two sections for configuration: :term:``mr.bob`` and :term:``variables``.

Example of global config file ``~/.mrbob`` or command line parameter ``mrbob --config foo.ini``.

.. code-block:: ini

    [mr.bob]
    verbose = True

    [variables]
    author.name = Domen Kožar
    author.email = domen@dev.si

Specifying answers
******************

To answer some questions from a config file instead of interactively. Given ``me.ini``:

.. code-block:: ini

    [variables]
    author.name = Domen Kožar
    author.email = domen@dev.si
    author.age = 24

do::

  $ mrbob --config me.ini mrbob:template_sample/

Specifying defaults
*******************

Sometimes you might want to override defaults for a template. Given ``me.ini``:

.. code-block:: ini

    [defaults]
    author.name = Domen Kožar
    author.email = domen@dev.si
    author.age = 24

do::

  $ mrbob --config me.ini mrbob:template_sample/

``mrbob`` will as you questions but default values will be also taken from config file.


Remote configuration
********************

Config file can also be loaded from a remote location::

  $ mrbob --config https://raw.github.com/iElectric/mr.bob/master/mrbob/tests/example.ini mrbob:template_sample/


Configuration inheritance
*************************

Configuration can be specified in multiple ways. See flow of mr.bob on the documentation front page to know how options are preferred.


Nesting variables into namespaces called groups
***********************************************

All variables can be specified in namespaces, such as ``author.name``. Currently namespaces
don't do anything special besides providing readability.



``mr.bob`` section reference
****************************

================  ===============================  =======================================================================
  Parameter         Default                          Explanation
================  ===============================  =======================================================================
ignored_files     No patterns                      Multiple Unix-style patterns to specify which files should be ignored:
                                                   for instance, to ignore, Vim swap files, specify ``*.swp``
non_interactive   False                            Don't prompt for input. Fail if questions are required but not answered
quiet             False                            Don't output anything except necessary
remember_answers  False                            Write answers to ``.mrbob.ini`` file inside output directory
verbose           False                            Output more information, useful for debugging
================  ===============================  =======================================================================



Collection of community managed templates
-----------------------------------------

You are encouraged to use the ``bobtemplates.something`` Python egg namespace to write
templates and contribute them to this list by making a `pull request <https://github.com/iElectric/mr.bob>`_.

- `bobtemplates.ielectric <https://github.com/iElectric/bobtemplates.ielectric>`_
- `bobtemplates.kotti <https://github.com/Kotti/bobtemplates.kotti>`_
- `bobtemplates.niteoweb <https://github.com/niteoweb/bobtemplates.niteoweb>`_


Collection of community plugins
-------------------------------

You are encouraged to use the ``bobplugins.something`` Python egg namespace to write
templates and contribute them to this list by making a `pull request <https://github.com/iElectric/mr.bob>`_.

- `bobplugins.jpcw <https://github.com/jpcw/bobplugins.jpcw>`_
