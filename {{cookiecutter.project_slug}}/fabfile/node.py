from fabric import task
from invoke import Collection


@task()
def install(ctx):
    """
    Install node package manager.
    """
    ctx.sudo('apt-get --yes install npm')


@task()
def configure(ctx):
    """
    Compile package.json
    """
    with ctx.cd(ctx.django_dir):
        ctx.run('npm install')


ns = Collection('node')
ns.add_task(install)
ns.add_task(configure)
