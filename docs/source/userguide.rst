.. highlight:: bash


User guide
==========

Installation
------------

::

    pip install mr.bob


Usage
-----


Once you install mr.bob, there is `mrbob` command available.

`$ mrbob --help`::

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

Most basic use case it rendering a template from a folder to current folder::

    $ mrbob template_folder/

Or from a package::

    $ mrbob some.package:template_folder/


Configuration
-------------

There are two types of configuration.

mr.bob
    configures how mr.bob behaves
variables
    populates variables that will be passed to templates

Configuration can be specified in multiple ways at the same time. 

::

    Global config at ~/.mrbob
        ^
        |
    `mrbob --config mrbob.ini`
        ^
        |
    `mrbob --some-variable foobar`
        ^
        |
    questions answered in interactive mode


Using configuration file
------------------------

Example of global config file `~/.mrbob` or command line parameter `mrbob --config foo-ini`.

::

    [mr.bob]
    non-interactive = true
    renderer = moo.foo:render_mako

    [variables]
    webserver.ip_addr = 10.0.10.120
    webserver.fqdn = briefkasten.10.0.10.120.xip.io
    webserver.foo.bar = briefkasten.10.0.10.120.xip.io
    webserver.foo.moo = briefkasten.10.0.10.120.xip.io

    [questions]
    webserver.ip_addr.question = Why o Why?
    webserver.ip_addr.default = True
    webserver.ip_addr.validator = foo.boo:validator_json
    webserver.ip_addr.help = Blabla blabal bal
    webserver.ip_addr.action = foo.boo:too
    webserver.ip_addr.prompt_command = getpass:getpass


Collection of community managed templates
-----------------------------------------


Design goals
------------

- Cover 80% of use cases, don't become too complex  
- Ability to use templates not only from eggs, but also folders and similar
- Python 3 support
- Jinja2 renderer by default, but replaceable
- Ability to render multiple templates to the same target directory
