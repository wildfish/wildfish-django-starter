Wildfish Django Starter
=======================

.. image:: https://travis-ci.org/wildfish/wildfish-django-starter.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/wildfish/wildfish-django-starter

A Django 2.0 friendly project cookiecutter template to kick start development
for new projects. Includes apps and settings we use in the majority of projects,
along with an integrated version of our other cookiecutter-django-crud template
which will also generate a model, CRUD views and tests.

Features
--------

* 2 tier layout
* Python essentials: ipython, ipdb, flake8
* Requirements file managed using pip-tools.
* Settings using django-configurations
* Testing bits: django-webtest, model-mommy
* Redis cache (via django-redis-cache)
* Sentry's raven client, django-debug-toolbar
* django-bootstrap3, django-model-utils
* Django CRUD views and templates using django-vanilla-views.
* A Django ModelForm using bootstrap3.
* Tests for all of the views using WebTest.
* Model Mommy generated models for the tests.
* Use Vagrant for 'local' deployments.
* Deploy to any server using Fabric and Invoke.


Quickstart
----------
Install Vagrant and virtualbox::

    sudo apt-get install vagrant virtualbox

Ensure you have cookiecutter and pip-tools installed::

    pip install cookiecutter
    pip install pip-tools

Then use cookiecutter to generate your project from this template with::

    cookiecutter git@github.com:wildfish/wildfish-django-starter.git

The Vagrant VM is assign a static IP address of 192.168.10.10. You will need
to add this address to your /etc/hosts file to access the web site::

    192.168.10.10 <project_slug>.local

where <project_slug> is the value you chose when generating the project from
the cookiecutter template.

Then from your generated project you can deploy the full project to a local
Vagrant instance using::

    pip-compile requirements.in

    vagrant up --provision

    vagrant ssh-config > ssh-config

    fab -H <project_slug>.local --ssh-config ssh-config deploy.full

Don't forget to replace <project_slug> with the actual value you used.

Requirements using pip-compile
------------------------------

The generated project uses a requirements.in file to make it straightforward
to keep pinned requirements up to date using the ``pip-compile`` command
from ``pip-tools``.

To generate a requirements.txt from your project simply use the ``pip-compile`` command.

Read more here, https://github.com/nvie/pip-tools#example-usage-for-pip-compile
