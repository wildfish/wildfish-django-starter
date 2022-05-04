from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html")),
    path(
        "{{cookiecutter.app_name}}/",
        include(
            "{{cookiecutter.project_name}}.{{cookiecutter.app_name}}.urls",
            namespace="{{cookiecutter.app_name}}",
        ),
    ),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
