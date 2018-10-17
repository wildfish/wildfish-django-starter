#!/bin/bash

# cookiecutter will overwrite the project if it already exists. That ensures
# the tests will run for each python version even if one fails. We also want
# to remove the generated project so that everything is left in a clean state.

set -e
py.test
cookiecutter . --no-input --overwrite-if-exists
cd new_project
npm install
pip install -r requirements.in
python manage.py makemigrations
python manage.py test
cd ..
rm -rf new_project
