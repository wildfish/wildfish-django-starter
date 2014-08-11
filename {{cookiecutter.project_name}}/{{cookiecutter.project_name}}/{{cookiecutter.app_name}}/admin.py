from django.contrib import admin
from .models import {{ cookiecutter.model_name }}

admin.site.register({{ cookiecutter.model_name }})

