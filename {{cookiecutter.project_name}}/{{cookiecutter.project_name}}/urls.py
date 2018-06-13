from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    path(r'', TemplateView.as_view(template_name='home.html')),
    path(r'{{cookiecutter.app_name}}/', include('{{cookiecutter.project_name}}.{{cookiecutter.app_name}}.urls', namespace='{{cookiecutter.app_name}}')),
    path(r'admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ]
