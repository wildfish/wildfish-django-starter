#!/bin/bash
set -e

# Test the cookiecutter project
pytest --cache-clear

# Create a project with cookie cutter then apply it's own pytest
cookiecutter ./ --no-input
cd newproject
pip install pip-tools
pip-compile requirements-dev.in -o requirements.txt
pip install -r requirements.txt
python manage.py makemigrations
pytest -vv

# Remove test project
cd ..
rm -rf newproject
