Wildfish Django Starter
=====================

A Django 1.7 friendly project cookiecutter template to kick start development for new projects.  Includes apps and settings we use in the majority of projects, along with an integrated version of our other cookiecutter-django-crud template which will also generate a model, CRUD views and tests.

Features
----------

* 2 tier layout
* Python essentials: ipython, ipdb, flake8
* Settings using django-configurations
* Testing bits: django-webtest, model-mommy
* Redis cache (via django-redis-cache)
* Sentry's raven client, django-debug-toolbar
* django-bootstrap3, django-model-utils
* Django CRUD views and templates using django-vanilla-views.
* A Django ModelForm using bootstrap3.
* Tests for all of the views using WebTest.
* Model Mommy generated models for the tests.


Quickstart
----------

Ensure you have cookiecutter installed, and then:

    cookiecutter git@github.com:wildfish/wildfish-django-starter.git
