#!/bin/bash
set -e

if [ -d newproject ]; then rm -Rf newproject; fi

# Test the cookiecutter project
pytest

# Create a project with cookie cutter then apply it's own pytest
cookiecutter ./ --no-input
cd newproject
pip install pip-tools
pip-compile requirements-dev.in -o requirements.txt
pip install -r requirements.txt
python manage.py makemigrations
pytest -vv
