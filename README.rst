Bob renders directory structure templates

INSTALL
=======

::

    $ pip install mrbob

USAGE
=====

DEVELOP
=======

::

    $ git clone https://github.com/iElectric/mr.bob.git mrbob
    $ cd mrbob
    $ virtualenv .
    $ source bin/activate
    $ python setup.py develop
    $ easy_install mrbob[test]

RUNNING TESTS
=============

::

    $ nosetests

TODO
====

- [high] Python 3 support
- [high] non interactive support
- [high] ability to use multiple templates at the same time
- [high] support pluggable rendering engine
- [low] ability to specify answers to questions from cli
- [low] ability to simulate rendering
- [low] ability to override templates
