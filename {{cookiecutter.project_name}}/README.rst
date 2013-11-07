Wildfish Django Starter
=====================

A Django 1.5 project template to kick start development for new projects.  Includes apps and settings useful for 9/10 projects.

Features
----------

* 2 tier layout
* Python essentials: ipython, ipdb, pep8
* Settings using django-configurations
* Testing bits: django-webtest, model-mommy, django-jenkins
* Redis cache (via django-redis-cache)
* Senty's raven client, django-debug-toolbar
* django-crispy-form, django-model-utils


Quickstart
----------

Replace projectname with the name of your new project.

Create a new virtualenv, and install our requirements - presumes use of virtualenvwrapper:

.. code-block:: console

    mkvirtualenv <projectname>
    pip install -r https://raw.github.com/wildfish/wildfish-django-starter/master/requirements.txt

Create your django project:

.. code-block:: console

    django-admin.py startproject --template=https://github.com/wildfish/wildfish-django-starter/archive/master.zip <projectname>
