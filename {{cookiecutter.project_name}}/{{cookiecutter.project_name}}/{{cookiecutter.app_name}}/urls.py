from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.{{ cookiecutter.model_name }}List.as_view(), name='list'),
    url(r'^new/$', views.{{ cookiecutter.model_name }}Create.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.{{ cookiecutter.model_name }}Detail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', views.{{ cookiecutter.model_name }}Update.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', views.{{ cookiecutter.model_name }}Delete.as_view(), name='delete'),
]
