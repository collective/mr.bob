#!/bin/bash
# TODO: stash changes before doing tests: http://codeinthehole.com/writing/tips-for-using-a-git-pre-commit-hook/

EXITCODE=0

function handle_exit {
    if [ $? -ne 0 ]; then
        EXITCODE=1
    fi
}

echo '====== Running tests ========='
py.test --cov mrbob mrbob/; handle_exit

echo '====== Running PyFlakes ======'
python setup.py flakes; handle_exit

echo '====== Running pep8 =========='
pep8 mrbob; handle_exit
pep8 *.py; handle_exit

if [ $EXITCODE -ne 0 ]; then
    exit 1
fi
