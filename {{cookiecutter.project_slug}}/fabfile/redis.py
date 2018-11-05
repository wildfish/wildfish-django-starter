from fabric import task
from invoke import Collection

from .base import apt_update


@task
def install(ctx):
    """
    Install redis.
    """
    apt_update(ctx)

    ctx.sudo('apt-get --yes install redis-server')


ns = Collection('redis')
ns.add_task(install)
