#!/bin/bash
py.test
cookiecutter ./ --no-input
cd newproject
python manage.py test
cd ..
rm -rf newproject
