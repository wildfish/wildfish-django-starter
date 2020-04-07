import re

from .base import DjangoCookieTestCase


class TestCookiecutterSubstitution(DjangoCookieTestCase):
    """Test that all cookiecutter instances are substituted"""

    def test_all_cookiecutter_instances_are_substituted(self):
        # Build a list containing absolute paths to the generated files
        paths = self.generate_project()

        # Construct the cookiecutter search pattern
        pattern = r"{{(\s?cookiecutter)[.](.*?)}}"
        re_obj = re.compile(pattern)

        # Assert that no match is found in any of the files
        for path in paths:
            f = open(path, "r")
            for line in f:
                match = re_obj.search(line)
                self.assertIsNone(
                    match, f"cookiecutter variable not replaced in {path}"
                )
            f.close()
