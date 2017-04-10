#!/bin/bash
set -e
py.test
cookiecutter ./ --no-input
cd newproject
python manage.py makemigrations
python manage.py test
cd ..
rm -rf newproject
