from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy
from {{cookiecutter.project_name}}.{{cookiecutter.app_name}}.models import {{cookiecutter.model_name}}


class {{cookiecutter.model_name}}ApiResolver(APITestCase):
    def test_get_{{cookiecutter.model_name|lower}}___all_results_are_returned(self):
        objs = mommy.make({{cookiecutter.model_name}}, _quantity=10)

        response = self.client.get(reverse('{{cookiecutter.app_name}}:api:v1:{{cookiecutter.model_name|lower}}-list'))
        response_objs = [{{cookiecutter.model_name}}.objects.get(id=o['id']) for o in response.data]

        self.assertEqual(objs, response_objs)

    def test_get_{{cookiecutter.model_name|lower}}_with_specific_id___data_for_the_correct_{{cookiecutter.model_name|lower}}_is_returned(self):
        obj = mommy.make({{cookiecutter.model_name}}, name='first')

        response = self.client.get(reverse('{{cookiecutter.app_name}}:api:v1:{{cookiecutter.model_name|lower}}-detail', args=(obj.id,)))

        self.assertEqual('first', response.data['name'])

    def test_post_{{cookiecutter.model_name|lower}}___response_is_forbidden(self):
        response = self.client.post(
            reverse('{{cookiecutter.app_name}}:api:v1:{{cookiecutter.model_name|lower}}-list'),
            data={
                'name': 'first'
            }
        )

        self.assertEqual(403, response.status_code)

    def test_update_{{cookiecutter.model_name|lower}}_with_specific_id___response_is_forbidden(self):
        obj = mommy.make({{cookiecutter.model_name}}, name='first')

        response = self.client.post(
            reverse('{{cookiecutter.app_name}}:api:v1:{{cookiecutter.model_name|lower}}-detail', args=(obj.id,)),
            data={
                'name': 'new'
            }
        )

        self.assertEqual(403, response.status_code)