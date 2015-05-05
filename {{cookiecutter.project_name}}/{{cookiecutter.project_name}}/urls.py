from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',  # noqa
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^{{cookiecutter.app_name}}/', include('{{cookiecutter.project_name}}.{{cookiecutter.app_name}}.urls', namespace='{{cookiecutter.app_name}}')),
    url(r'^search/', include('haystack.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
