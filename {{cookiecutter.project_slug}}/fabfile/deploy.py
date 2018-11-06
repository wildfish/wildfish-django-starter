from fabric import task
from invoke import Collection

from fabfile import celery
from fabfile import git
from fabfile import nginx
from fabfile import python
from fabfile import postgres
from fabfile import project
from fabfile import supervisor
from fabfile import uwsgi
from fabfile import virtualenv
from fabfile import node


@task
def full(ctx):
    """
    Install all the system packages.
    """
    python.install(ctx)
    postgres.install(ctx)
    postgres.create(ctx)
    supervisor.install(ctx)
    nginx.install(ctx)
    git.install(ctx)
    virtualenv.install(ctx)
    node.install(ctx)
    project.create(ctx)
    virtualenv.create(ctx)
    uwsgi.install(ctx)

    if ctx.repository_url:
        project.checkout(ctx)
    else:
        project.upload(ctx)

    celery.configure(ctx)
    nginx.configure(ctx)
    uwsgi.configure(ctx)
    node.configure(ctx)
    project.requirements(ctx)
    project.collectstatic(ctx)
    project.migrate(ctx)
    project.permissions(ctx)
    nginx.restart(ctx)
    supervisor.restart(ctx)


ns = Collection('deploy')
ns.add_task(full)
