.. highlight:: bash

Developer guide
===============

Setup developer environment
---------------------------

::

    $ git clone https://github.com/iElectric/mr.bob.git
    $ cd mrbob
    $ virtualenv .
    $ source bin/activate
    $ pip install -e . [test,development]
    $ mrbob --help


Running tests
-------------

Easy as::

    $ make test


Making a Release
----------------

Using `zest.releaser`::

    $ bin/fullrelease
