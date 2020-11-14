#!/usr/bin/env bash

chmod 777 "$PWD/test.sh"
ln -sf "$PWD/test.sh" .git/hooks/pre-push

echo 'Executing pre-push hook.'

if [ -f "$PWD/venv/bin/activate" ]; then
    source $PWD/venv/bin/activate
fi


if black --check --target-version py37 -l 120 --exclude venv .
then
    echo 'Black passed ✅'
else
    echo 'Black failed ❌'
    echo 'RUN: black --target-version py37 -l 120 --exclude venv .'
    exit 1
fi


if pylint ./app ./encoder
then
    echo 'Pylint passed ✅'
else
    echo 'Pylint failed ❌'
    exit 1
fi


# TODO: Make tests.
#if coverage run manage.py test
#then
#    echo 'Django tests passed ✅'
#else
#    echo 'Django tests failed ❌'
#    exit 1
#fi
#
#coverage report -m
#
#coverage html

#if dredd;
#then
#    echo 'Dredd passed ✅'
#else
#    echo 'Dredd failed ❌'
#    exit 1
#fi

echo 'Well done.'

