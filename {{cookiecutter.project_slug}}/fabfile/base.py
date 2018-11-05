from fabric import task


@task
def apt_update(ctx):
    """
    Get the latest system package information.
    """
    ctx.sudo('apt-get update')
