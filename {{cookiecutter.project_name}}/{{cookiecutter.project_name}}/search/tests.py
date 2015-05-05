from django.core.urlresolvers import reverse
from django_webtest import WebTest
from model_mommy import mommy


class SearchTest(WebTest):
    def setUp(self):
        self.instance = mommy.make('{{cookiecutter.model_name}}')

    def _search(self, criteria):
        """
        Submits a search and returns a list of event pks.
        """
        response = self.app.get(reverse('haystack_search'))
        form = response.forms['search_form']
        form.fields.update(criteria)
        response = form.submit()
        return response.context['results']

    def test_search_empty(self):
        criteria = {'q': ''}
        self.assertIn(self.instance.pk, self._search(criteria))

    def test_search(self):
        criteria = {'q': 'Example'}
        self.assertIn(self.instance.pk, self._search(criteria))
