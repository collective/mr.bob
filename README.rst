Mister Bob the Builder renders directory structure templates.

INSTALL
=======

::

    $ pip install mr.bob

USAGE
=====

Configuration
-------------

There are two types of configuration.

mr.bob
    configures how mr.bob behaves
variables
    populates variables that will be passed to templates

Configuration can be specified in multiple ways at the same time. 

Global config -> config passed to mr.bob -> mr.bob variables passed in CLI -> questions answered in interactive mode


Using configuration file
------------------------

Example of global `~/.mrbob` or ``--config foo.ini` passed to mrbob command line.

::

    [mr.bob]
    non-interactive = true
    renderer = moo.foo:render_mako

    [variables]
    webserver.ip_addr = 10.0.10.120
    webserver.fqdn = briefkasten.10.0.10.120.xip.io
    webserver.foo.bar = briefkasten.10.0.10.120.xip.io
    webserver.foo.moo = briefkasten.10.0.10.120.xip.io

DEVELOP
=======

::

    $ git clone https://github.com/iElectric/mr.bob.git mrbob
    $ cd mrbob
    $ virtualenv .
    $ source bin/activate
    $ python setup.py develop
    $ easy_install mr.bob[test]

RUNNING TESTS
=============

::

    $ nosetests

TODO
====

- [high] Python 3 support
- [high] non-interactive support
- [high] ability to configure what to ignore when copying templates
- [high] ability to have variable substitution in template names
- [high] ability to use multiple templates at the same time and depend on them
- [low] ability to specify answers to questions from cli
- [low] ability to simulate rendering
- [low] ability to override templates
