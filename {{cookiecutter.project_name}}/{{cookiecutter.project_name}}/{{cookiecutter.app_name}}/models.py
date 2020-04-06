from django.db import models
from django.urls import reverse


class {{ cookiecutter.model_name }}(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = (
            "name",
            "pk",
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("{{ cookiecutter.app_name }}:detail", args=[str(self.id)])
