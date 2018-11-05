from django.urls import path
from . import views


urlpatterns = [
    path(r'', views.{{cookiecutter.model_name}}List.as_view(), name='list'),
    path(r'new/', views.{{cookiecutter.model_name}}Create.as_view(), name='create'),
    path(r'<int:pk>/', views.{{cookiecutter.model_name}}Detail.as_view(), name='detail'),
    path(r'<int:pk>/update/', views.{{cookiecutter.model_name}}Update.as_view(), name='update'),
    path(r'<int:pk>/delete/', views.{{cookiecutter.model_name}}Delete.as_view(), name='delete'),
]


app_name = '{{cookiecutter.app_name}}'
