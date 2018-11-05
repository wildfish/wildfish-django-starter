from fabric import task
from invoke import Collection

from .base import apt_update


def add_ppa(ctx):
    """
    Add external repositories for downloading system packages.
    """
    ctx.sudo('add-apt-repository ppa:deadsnakes/ppa')

    apt_update(ctx)


@task()
def install(ctx):
    """
    Install python and all the packages needed for building and installing dependencies.
    """
    add_ppa(ctx)

    packages = ' '.join([
        'python%s' % ctx.python_version,
        'python%s-dev' % ctx.python_version,
        'python-setuptools',
        'python-pip',
        'build-essential'
    ])

    ctx.sudo('apt-get --yes install %s' % packages)


ns = Collection('python')
ns.add_task(install)
