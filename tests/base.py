import os
import shutil
import unittest
from os.path import dirname, exists, join

import sh
from cookiecutter.main import cookiecutter


class DjangoCookieTestCase(unittest.TestCase):

    root_dir = dirname(dirname(__file__))
    destpath = None

    def generate_project(self, extra_context=None):
        ctx = {
            "project_title": "Some New Project",
            "project_name": "thenewtestproject",
            "author_name": "Your name",
            "author_email": "you@somewhere.com",
            "domain_name": "wildfish.com",
            "time_zone": "Europe/London",
            "email_user": "",
            "email_password": "",
            "sentry_dsn": "",
            "app_name": "testthings",
            "model_name": "TestThing",
            "django_version": "LTS (3.2)",
        }

        if extra_context:
            assert isinstance(extra_context, dict)
            ctx.update(extra_context)

        self.ctx = ctx
        self.destpath = join(self.root_dir, self.ctx["project_name"])

        cookiecutter(template="./", checkout=None, no_input=True, extra_context=ctx)

        # Build a list containing absolute paths to the generated files
        paths = [
            os.path.join(dirpath, file_path)
            for dirpath, subdirs, files in os.walk(self.destpath)
            for file_path in files
        ]
        return paths

    def clean(self):
        if exists(self.destpath):
            shutil.rmtree(self.destpath)
        sh.cd(self.root_dir)

    def tearDown(self):
        self.clean()
