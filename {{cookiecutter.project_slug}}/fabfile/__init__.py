from invoke import Collection

from fabfile.celery import ns as celery_ns
from fabfile.git import ns as git_ns
from fabfile.nginx import ns as nginx_ns
from fabfile.node import ns as node_ns
from fabfile.postgres import ns as postgres_ns
from fabfile.project import  ns as project_ns
from fabfile.python import ns as python_ns
from fabfile.redis import ns as redis_ns
from fabfile.supervisor import ns as supervisor_ns
from fabfile.uwsgi import ns as uwsgi_ns
from fabfile.virtualenv import ns as virtualenv_ns
from fabfile.deploy import ns as deploy_ns

ns = Collection()
ns.add_collection(celery_ns)
ns.add_collection(git_ns)
ns.add_collection(nginx_ns)
ns.add_collection(postgres_ns)
ns.add_collection(project_ns)
ns.add_collection(python_ns)
ns.add_collection(redis_ns)
ns.add_collection(supervisor_ns)
ns.add_collection(uwsgi_ns)
ns.add_collection(virtualenv_ns)
ns.add_collection(node_ns)
ns.add_collection(deploy_ns)
