.. highlight:: bash


User guide
==========


Installation
------------

:: pip install mr.bob


Usage
-----


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

Example of global `~/.mrbob` or `mrbob --config foo-ini`.

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


Design goals
------------



Reporting bugs
--------------

Check if an issue already exists at https://github.com/iElectric/almir/issues,
otherwise add new one with following information: 

* bacula-director version, operating system and browser version
* include screenshot if it provides any useful information
* pastebin (http://paste2.org) output of $ cat ALMIR_ROOT/var/logs/almir-stderr*
* pastebin ALMIR_ROOT/buildout.cfg, but be careful to *remove any sensitive data*
