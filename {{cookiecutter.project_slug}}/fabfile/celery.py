from fabric import task
from invoke import Collection

from fabfile.utils import render_template


@task()
def configure(ctx):
    """
    Add the configuration files celery to supervisor.
    """
    contents = render_template('etc/celery.conf', ctx)
    ctx.put(contents, '%s/celery.conf' % ctx.install_dir)

    contents = render_template('etc/celerybeat.conf', ctx)
    ctx.put(contents, '%s/celerybeat.conf' % ctx.install_dir)

    supervisor_dir = '/etc/supervisor/conf.d'

    ctx.sudo('mv %s/celery.conf %s/celery_%s.conf' % (ctx.install_dir, supervisor_dir, ctx.project_slug))
    ctx.sudo('mv %s/celerybeat.conf %s/celerybeat_%s.conf' % (ctx.install_dir, supervisor_dir, ctx.project_slug))


@task()
def restart(ctx):
    """
    Restart celery workers and celery beat.
    """
    ctx.sudo('supervisorctl restart celery_%s' % ctx.project_slug)
    ctx.sudo('supervisorctl restart celerybeat_%s' % ctx.project_slug)


ns = Collection('celery')
ns.add_task(configure)
ns.add_task(restart)
