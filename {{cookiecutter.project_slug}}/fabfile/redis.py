from fabric import task
from invoke import Collection


@task
def install(ctx):
    """
    Install redis.
    """
    ctx.sudo('apt-get --yes install redis-server')


ns = Collection('redis')
ns.add_task(install)
