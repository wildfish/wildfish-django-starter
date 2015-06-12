from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django_webtest import WebTest


class RegistrationTests(WebTest):
    def test_registration(self):
        """
        Test that we can register a new account.
        """
        User = get_user_model()
        response = self.app.get(reverse('account_signup'))

        email = 'dirk@wildfish.com'

        # check that we don't already have a model with this name
        self.assertFalse(User.objects.filter(email=email).exists())

        # create an entry via the create form
        form = response.forms[0]
        form['username'] = 'dirk'
        form['email'] = email
        form['password1'] = 'topsecret'
        form['password2'] = 'topsecret'
        form.submit().follow()

        # check that our new entry now exists
        instance = User.objects.get(email=email)
        self.assertEqual(instance.email, email)
