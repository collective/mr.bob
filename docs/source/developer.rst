.. highlight:: bash

Developer guide
===============

Setup developer environment
---------------------------

::

    $ git clone https://github.com/iElectric/mr.bob.git mrbob
    $ cd mrbob
    $ virtualenv .
    $ source bin/activate
    $ python setup.py develop
    $ easy_install mr.bob[test,development]
    $ mrbob --help


Running tests
-------------

Easy as::

    $ ./bin/test


Make a Release
--------------

::

    $ bin/fullrelease
