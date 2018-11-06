from contextlib import contextmanager as _contextmanager
from fabric import task
from invoke import Collection

# We don't want to upgrade the latest version of pip as that currently
# breaks. See, https://github.com/pypa/pip/issues/5240. Basically pip
# moved the main() function to an internal package and that triggers all
# kinds of chaos.


@_contextmanager
def virtualenv(ctx):
    """
    Activate the virtualenv for running a command.
    """
    with ctx.cd(ctx.virtualenv_dir):
        with ctx.prefix('source %s/bin/activate' % ctx.virtualenv_dir):
            yield


@task
def install(ctx):
    """
    Install the virtualenv package.
    """
    ctx.sudo('apt-get --yes install virtualenv')


@task
def create(ctx):
    """
    Create the virtualenv.
    """
    with ctx.cd(ctx.install_dir):
        ctx.run('virtualenv --python=python%s %s' % (ctx.python_version, ctx.virtualenv_dir))


@task
def remove(ctx):
    """
    Remove the virtualenv.
    """
    ctx.sudo('rm -rf %s' % ctx.virtualenv_dir)


ns = Collection('virtualenv')
ns.add_task(install)
ns.add_task(create)
ns.add_task(remove)
