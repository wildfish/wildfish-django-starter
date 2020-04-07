from django.urls import reverse

import pytest
from model_bakery import baker

from ..models import {{cookiecutter.model_name}}


# All tests require the database
pytestmark = pytest.mark.django_db


def test_factory_create(django_app):
    """
    Test that we can create an instance via our object factory.
    """
    instance = baker.make({{cookiecutter.model_name}})
    assert isinstance(instance, {{cookiecutter.model_name}})


def test_list_view(django_app):
    """
    Test that the list view returns at least our factory created instance.
    """
    instance = baker.make({{cookiecutter.model_name}})
    response = django_app.get(reverse("{{cookiecutter.app_name}}:list"))
    object_list = response.context["object_list"]
    assert instance in object_list


def test_create_view(django_app):
    """
    Test that we can create an instance via the create view.
    """
    response = django_app.get(reverse("{{cookiecutter.app_name}}:create"))
    new_name = "A freshly created {{cookiecutter.model_name}}"

    # check that we don"t already have a model with this name
    assert not {{cookiecutter.model_name}}.objects.filter(name=new_name).exists()

    form = response.forms["{{cookiecutter.model_name_lower}}_form"]
    form["name"] = new_name
    form.submit().follow()

    instance = {{cookiecutter.model_name}}.objects.get(name=new_name)
    assert instance.name == new_name


def test_detail_view(django_app):
    """
    Test that we can view an instance via the detail view.
    """
    instance = baker.make({{cookiecutter.model_name}})
    response = django_app.get(instance.get_absolute_url())
    assert response.context["object"] == instance


def test_update_view(django_app):
    """
    Test that we can update an instance via the update view.
    """
    instance = baker.make({{cookiecutter.model_name}})
    response = django_app.get(reverse("{{cookiecutter.app_name}}:update", kwargs={"pk": instance.pk}))
    print(response.forms)
    form = response.forms["{{cookiecutter.model_name_lower}}_form"]
    new_name = "Some new {{cookiecutter.model_name}}"
    form["name"] = new_name
    form.submit().follow()

    instance = {{cookiecutter.model_name}}.objects.get(pk=instance.pk)
    assert instance.name == new_name


def test_delete_view(django_app):
    """
    Test that we can delete an instance via the delete view.
    """
    instance = baker.make({{cookiecutter.model_name}})
    pk = instance.pk
    response = django_app.get(reverse("{{cookiecutter.app_name}}:delete", kwargs={"pk": pk}))
    response.form.submit().follow()
    assert not {{cookiecutter.model_name}}.objects.filter(pk=pk).exists()
