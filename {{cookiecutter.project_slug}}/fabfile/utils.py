import os

from jinja2 import Environment, FileSystemLoader
from six import StringIO


def render_template(template, context):
    env = Environment(loader=FileSystemLoader(os.getcwd()))
    template = env.get_template(template)
    return StringIO(template.render(ctx=context))
