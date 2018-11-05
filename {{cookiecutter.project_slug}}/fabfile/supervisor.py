from fabric import task
from invoke import Collection

from .base import apt_update


@task
def install(ctx):
    """
    Install supervisor.
    """
    apt_update(ctx)

    ctx.sudo('apt-get --yes install supervisor')


@task
def restart(ctx):
    """
    Reload the supervisor configurations.

    We assume there may be new or discontinued services so a full
    reload and restart of all services is performed.
    """
    ctx.sudo('supervisorctl reread')
    ctx.sudo('supervisorctl update')


ns = Collection('supervisor')
ns.add_task(install)
ns.add_task(restart)
