Mister Bob the Builder renders directory structure templates.

INSTALL
=======

::

    $ pip install mr.bob

USAGE
=====

TODO: document that jinja templating has extra configuration


DESIGN DESCRIPTION
==================


Configuration
-------------

There are two types of configuration.

mr.bob
    configures how mr.bob behaves
variables
    populates variables that will be passed to templates

Configuration can be specified in multiple ways at the same time. 

::

    Global config
        ^
        |
    config passed to mr.bob
        ^
        |
    mr.bob variables passed in CLI
        ^
        |
    questions answered in interactive mode


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

    [questions]
    webserver.ip_addr.question = Why o Why?
    webserver.ip_addr.default = True
    webserver.ip_addr.validator = foo.boo:validator_json
    webserver.ip_addr.help = Blabla blabal bal
    webserver.ip_addr.action = foo.boo:too
    webserver.ip_addr.prompt_command = getpass:getpass


Terminology
===========

bobconfig

variables == answers

questions

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
- [high] write usermanual/developermanual (diagram how it works)
- [high] non-interactive support (disable last phase of configuration)
- [high] ability to configure what to ignore when copying templates
- [high] ability to use multiple templates at the same time and depend on them
- [low] ability to have localcommands
- [low] ability to remember answers for the rendered template
- [low] ability to specify pre/post functions when rendering templates
- [low] ability to specify actions to answers, for example if one question was answered, another template may be triggered
- [low] ability to specify answers to questions from cli
- [low] ability to simulate rendering
- [low] ability to override templates
