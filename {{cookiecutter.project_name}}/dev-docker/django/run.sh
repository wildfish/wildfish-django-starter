#!/bin/bash
cd /project

./manage.py migrate
./manage.py runserver 0:8000