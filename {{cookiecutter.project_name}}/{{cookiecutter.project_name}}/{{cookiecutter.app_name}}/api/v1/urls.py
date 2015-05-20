from django.conf.urls import url, include, patterns
from rest_framework import routers
from {{cookiecutter.project_name}}.{{cookiecutter.app_name}}.api.v1.{{cookiecutter.model_name|lower}} import ViewSet as {{cookiecutter.model_name}}ViewSet

v1_router = routers.SimpleRouter()
v1_router.register(r'{{cookiecutter.model_name|lower}}', {{cookiecutter.model_name}}ViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(v1_router.urls)),
)
