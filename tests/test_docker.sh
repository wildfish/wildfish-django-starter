#!/bin/sh
set -o errexit

if [ -d newproject ]; then rm -Rf newproject; fi

# install test requirements
pip install -r requirements.txt

cookiecutter . --no-input
cd newproject
cp dev-docker-compose.yml.default dev-docker-compose.yml
pip-compile requirements.in -o requirements.txt

# run the tests with this config
docker-compose -f dev-docker-compose.yml run django pytest -vv

cd ../
rm -rf newproject
