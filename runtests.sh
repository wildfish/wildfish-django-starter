#!/bin/bash
set -e

if [ -d newproject ]; then rm -Rf newproject; fi

# Test the cookiecutter project
pytest -vv

# Create a project with cookie cutter then apply it's own pytest
cookiecutter ./ --no-input
cd newproject

# install the requirements, note Django is removed so we trust the tox/travis version
sed '1,/django/s/django/'"${TOX_DJANGO_VERSION:-django>=3.0, <3.1}"'/' requirements.in > /tmp/req.in
pip-compile /tmp/req.in -o /tmp/req.txt
pip install -r /tmp/req.txt

# migrate then test
python manage.py makemigrations
pytest -vv

cd ../
rm -rf newproject