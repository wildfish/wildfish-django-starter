from fabric import task
from invoke import Collection

from fabfile.utils import render_template


@task()
def install(ctx):
    """
    Install nginx.
    """
    ctx.sudo('apt-get --yes install nginx')


@task()
def configure(ctx):
    """
    Add the configuration file for the site to nginx.
    """
    site_available = '/etc/nginx/sites-available/%s' % ctx.project_slug
    site_enabled = '/etc/nginx/sites-enabled/%s' % ctx.project_slug

    contents = render_template('etc/nginx.conf', ctx)
    ctx.put(contents, '%s/nginx.conf' % ctx.install_dir)

    ctx.sudo('mv %s/nginx.conf  %s' % (ctx.install_dir, site_available))
    ctx.sudo('ln -fs %s %s' % (site_available, site_enabled))
    ctx.sudo('rm -f /etc/nginx/sites-enabled/default')

    if ctx.use_local_certificate:
        with ctx.cd(ctx.django_dir):
            ctx.run('openssl req -x509 -out project.crt -keyout project.key'
                    ' -newkey rsa:2048 -nodes -sha256'
                    ' -subj \'/CN={{cookiecutter.domain}}\' -extensions EXT -config <('
                    ' printf "[dn]\nCN={{cookiecutter.domain}}\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:{{cookiecutter.domain}}\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")')


@task()
def restart(ctx):
    """
    Reload nginx config.
    """
    ctx.sudo('/etc/init.d/nginx reload')


ns = Collection('nginx')
ns.add_task(install)
ns.add_task(configure)
ns.add_task(restart)
