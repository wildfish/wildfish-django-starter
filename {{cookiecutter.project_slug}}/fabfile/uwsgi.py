from fabric import task
from invoke import Collection

from fabfile.utils import render_template
from fabfile.virtualenv import virtualenv


@task
def install(ctx):
    """
    Install uwsgi in the virtualenv
    """
    with virtualenv(ctx):
        ctx.run('pip install uwsgi')


@task()
def configure(ctx):
    """
    Add the configuration file for uwsgi to supervisor.
    """
    contents = render_template('etc/uwsgi.conf', ctx)
    ctx.put(contents, '%s/uwsgi.conf' % ctx.install_dir)

    contents = render_template('etc/uwsgi.ini', ctx)
    ctx.put(contents, '%s/uwsgi.ini' % ctx.django_dir)

    supervisor_dir = '/etc/supervisor/conf.d'

    ctx.sudo('mv %s/uwsgi.conf %s/uwsgi_%s.conf' % (ctx.install_dir, supervisor_dir, ctx.project_slug))


@task()
def restart(ctx):
    """
    Graceful restart of wsgi server.
    """
    ctx.run('touch %s/uwsgi.reload' % ctx.run_dir)


ns = Collection('uwsgi')
ns.add_task(install)
ns.add_task(configure)
ns.add_task(restart)
