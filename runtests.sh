#!/bin/bash
set -e

if [ -d newproject ]; then rm -Rf newproject; fi

# Test the cookiecutter project
pytest -vv

# Create a project with cookie cutter then apply it's own pytest
cookiecutter ./ --no-input
cd newproject

# install the requirements, remove whatever Django is used and force in the tox version.
sed 's/django>=.*/'"${TOX_DJANGO_VERSION}"'/g' requirements.in > /tmp/req.in
pip-compile /tmp/req.in -o /tmp/req.txt
pip install -r /tmp/req.txt

# migrate then test
python manage.py makemigrations
pytest -vv

cd ../
rm -rf newproject