from fabric import task
from invoke import Collection


@task
def install(ctx):
    """
    Install git.
    """
    ctx.sudo('apt-get --yes install git')


ns = Collection('git')
ns.add_task(install)
