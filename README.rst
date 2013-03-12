Wildfish Django Starter
=====================

A Django 1.5 project template to begin development from.

Quickstart
----------

Replace projectname with the name of your new project.

Create a new virtualenv with our requirements - presumes use of virtualenvwrapper:

.. code-block:: console

    mkvirtualenv -r https://raw.github.com/wildfish/wildfish-django-starter/master/requirements.txt projectname

Create your django project:

.. code-block:: console

    django-admin.py startproject --template=https://github.com/wildfish/wildfish-django-starter/archive/master.zip projectname
