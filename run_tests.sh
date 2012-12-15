#!/bin/bash
# TODO: stash changes before doing tests: http://codeinthehole.com/writing/tips-for-using-a-git-pre-commit-hook/

EXITCODE=0

function handle_exit {
    if [ $? -ne 0 ]; then
        EXITCODE=1
    fi
}

echo '====== Running tests ========='
bin/nosetests $@; handle_exit

echo '====== Running flake8 ======'
bin/flake8 *.py; handle_exit
bin/flake8 mrbob; handle_exit

if [ $EXITCODE -ne 0 ]; then
    exit 1
fi
