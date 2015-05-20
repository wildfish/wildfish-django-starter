from django.core.urlresolvers import reverse_lazy
from vanilla import TemplateView, CreateView, DetailView, UpdateView, DeleteView
from .forms import {{ cookiecutter.model_name }}Form
from .models import {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}List(TemplateView):
    template_name = '{{cookiecutter.app_name}}/{{cookiecutter.model_name|lower}}_list.html'


class {{ cookiecutter.model_name }}Create(CreateView):
    model = {{ cookiecutter.model_name }}
    form_class = {{ cookiecutter.model_name }}Form
    success_url = reverse_lazy('{{ cookiecutter.app_name }}:list')


class {{ cookiecutter.model_name }}Detail(DetailView):
    model = {{ cookiecutter.model_name }}


class {{ cookiecutter.model_name }}Update(UpdateView):
    model = {{ cookiecutter.model_name }}
    form_class = {{ cookiecutter.model_name }}Form
    success_url = reverse_lazy('{{ cookiecutter.app_name }}:list')


class {{ cookiecutter.model_name }}Delete(DeleteView):
    model = {{ cookiecutter.model_name }}
    success_url = reverse_lazy('{{ cookiecutter.app_name }}:list')
