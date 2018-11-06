from fabric import task
from invoke import Collection

from fabfile.virtualenv import virtualenv


@task
def create(ctx):
    """
    Create the user account and directories for the project.
    """
    ctx.sudo('id -u {0} &>/dev/null || sudo useradd {0} -s /bin/bash'.format(ctx.host_user))

    ctx.run('mkdir -p %s' % ctx.install_dir)
    ctx.run('mkdir -p %s' % ctx.django_dir)
    ctx.run('mkdir -p %s' % ctx.media_dir)
    ctx.run('mkdir -p %s' % ctx.static_dir)
    ctx.run('mkdir -p %s' % ctx.log_dir)
    ctx.run('mkdir -p %s' % ctx.run_dir)


@task
def permissions(ctx):
    """
    Fix the permissions for the project.
    """
    ctx.sudo('chown -R {0}:{0} {1}'.format(ctx.host_user, ctx.install_dir))
    ctx.sudo('chmod 777 %s/.' % ctx.run_dir)


@task
def upload(ctx):
    """
    Tar up the project and upload it to the server.
    """
    package_file = '%s.tar.gz' % ctx.project_slug
    excludes = "--exclude='.vagrant' --exclude='fabfile' --exclude='etc' --exclude='Vagrantfile'"

    ctx.local("tar -czf /tmp/%s %s ." % (package_file, excludes))

    ctx.put('/tmp/%s' % package_file, '.')
    ctx.run('mv %s %s' % (package_file, ctx.django_dir))

    with ctx.cd(ctx.django_dir):
        ctx.run('tar -xzf %s' % package_file)
        ctx.run('rm %s' % package_file)

    ctx.local('rm /tmp/%s' % package_file)


@task
def checkout(ctx):
    """
    Checkout the app from the repository.
    """
    with ctx.cd(ctx.install_dir):
        ctx.run('git clone --branch %s %s %s' % (
            ctx.repository_branch, ctx.repository_url, ctx.project_slug))


@task
def requirements(ctx):
    """
    Install the pip requirements in the python virtualenv.
    """
    with virtualenv(ctx):
        ctx.run('pip install -r %s' % ctx.requirements_file)


@task
def collectstatic(ctx):
    """
    Collect static files.
    """
    with virtualenv(ctx):
        with ctx.cd(ctx.django_dir):
            ctx.run('./manage.py collectstatic -v 2 --noinput')


@task
def migrate(ctx):
    """
    Run the database migrations.
    """
    with virtualenv(ctx):
        with ctx.cd(ctx.django_dir):
            ctx.run('./manage.py migrate')


ns = Collection('project')
ns.add_task(create)
ns.add_task(upload)
ns.add_task(checkout)
ns.add_task(requirements)
ns.add_task(collectstatic)
ns.add_task(migrate)
