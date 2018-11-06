#!/bin/env python

import os
import random
import string

from jinja2 import Environment, FileSystemLoader


def render_template(template, context):
    env = Environment(loader=FileSystemLoader(os.getcwd()))
    template = env.get_template(template)
    return template.render(**context)


if __name__ == '__main__':

    settings_path = '{{cookiecutter.project_slug }}/settings.py'

    secret_key = ''.join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        ) for _ in range(64)
    )

    settings = render_template(settings_path, {
        'secret_key': secret_key
    })

    with open(settings_path, 'wb') as fh:
        fh.write(settings.encode('utf-8'))

