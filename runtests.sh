#!/bin/bash
set -e

if [ -d newproject ]; then rm -Rf newproject; fi

if [ -z "$TOX_DJANGO_VERSION" ]
then
      TOX_DJANGO_VERSION='django>=3.0, <3.1'
fi

# Test the cookiecutter project
pytest -vv

# Create a project with cookie cutter then apply it's own pytest
cookiecutter ./ --no-input
cd newproject

# install the requirements, note Django is removed so we trust the tox/travis version
sed -i '' '1,/django/s/django/'"$TOX_DJANGO_VERSION"'/' requirements.in
pip-compile requirements.in -o requirements.txt
pip install -r requirements.txt

# migrate then test
python manage.py makemigrations
pytest -vv

cd ../
rm -rf newproject