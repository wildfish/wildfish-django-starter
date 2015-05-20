from django.conf.urls import patterns, url, include


urlpatterns = patterns(
    '',

    url("^v1/", include('{{cookiecutter.project_name}}.{{cookiecutter.app_name}}.api.v1.urls', namespace='v1')),
)