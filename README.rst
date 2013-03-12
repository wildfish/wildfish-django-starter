Wildfish Django Starter
=====================

A baseline Djagno 1.5 project to begin development from.

Quickstart
----------

Replace projectname with the name of your new project.

Create a new virtualenv with our requirements - presumes use of virtualenvwrapper:

.. code-block:: console

    mkvirtualenv -r https://raw.github.com/wildfish/wildfish-django-starter/master/requirements.txt projectname

Create your django project:

.. code-block:: console

    django-admin.py startproject --template=https://github.com/wildfish/wildfish-django-starter/archive/master.zip projectname
