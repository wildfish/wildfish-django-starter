from fabric import task
from invoke import Collection

from .base import apt_update


@task
def install(ctx):
    """
    Install git.
    """
    apt_update(ctx)

    ctx.sudo('apt-get --yes install git')


ns = Collection('git')
ns.add_task(install)
