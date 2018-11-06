from fabric import task
from invoke import Collection


def add_ppa(ctx):
    """
    Add external repositories for downloading system packages.
    """
    ctx.sudo('add-apt-repository ppa:deadsnakes/ppa')


@task()
def install(ctx):
    """
    Install python and all the packages needed for building and installing dependencies.
    """
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
