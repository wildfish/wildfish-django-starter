from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^{{cookiecutter.app_name}}/', include('{{cookiecutter.project_name}}.{{cookiecutter.app_name}}.urls', namespace='{{cookiecutter.app_name}}')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
