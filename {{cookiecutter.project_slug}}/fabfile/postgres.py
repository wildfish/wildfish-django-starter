import datetime
import os

from fabric import task
from invoke import Collection


# TODO Add task to drop database
# TODO Add task to restore database


@task
def install(ctx):
    """
    Install the database, contrib packages and python driver.
    """
    ctx.sudo('apt-get --yes install postgresql postgresql-contrib python-psycopg2')
    ctx.sudo('psql -c "SELECT version();"', user='postgres')


@task
def create_user(ctx):
    """
    Create the database owner, if it does not exist.
    """
    sql = "SELECT 1 FROM pg_roles WHERE rolname='%s'" % ctx.db_user
    result = ctx.sudo('psql -tc "%s"' % sql, user='postgres', hide=True)
    if not result.stdout.strip():
        cmd = 'psql -c "CREATE ROLE %s WITH ENCRYPTED PASSWORD \'%s\';"' % (ctx.db_user, ctx.db_pass)
        ctx.sudo(cmd, user='postgres')


@task
def create_db(ctx):
    """
    Create the database, if it does not exist.
    """
    sql = "SELECT 1 from pg_database WHERE datname='%s';" % ctx.db_name
    result = ctx.sudo('psql -tc "%s"' % sql, user='postgres', hide=True)
    if not result.stdout.strip():
        cmd = 'psql -c "CREATE DATABASE %s WITH OWNER %s;"' % (ctx.db_name, ctx.db_user)
        ctx.sudo(cmd, user='postgres')


@task
def create(ctx):
    """
    Create the project database and user.
    """
    create_user(ctx)
    create_db(ctx)


@task
def drop_user(ctx):
    """
    Drop the database owner.
    """
    cmd = 'psql --command "drop user %s;"' % ctx.db_user
    ctx.sudo(cmd, user='postgres')


@task
def drop_db(ctx):
    """
    Drop the database.
    """
    cmd = 'psql --command "drop database %s;"' % ctx.db_name
    ctx.sudo(cmd, user='postgres')


@task
def drop(ctx):
    """
    Drop the project database and user.
    """
    drop_db(ctx)
    drop_user(ctx)


@task
def dump(ctx):
    """
    Dump the database.
    """
    cmd = 'pg_dump --clean --no-owner --file %s %s' % (ctx.db_file, ctx.db_name)
    ctx.sudo(cmd, user='postgres')


@task
def download(ctx):
    """
    Download the database
    """
    ctx.get(ctx.db_file, os.path.basename(ctx.db_file))
    ctx.sudo('rm %s' % ctx.db_file, user='postgres')


@task
def backup(ctx):
    """
    Backup the database
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    ctx.db_file = '/tmp/{}-{}.sql'.format(ctx.db_name, timestamp)

    dump(ctx)
    download(ctx)


ns = Collection('postgres')
ns.add_task(install)
ns.add_task(create)
ns.add_task(drop)
ns.add_task(backup)
