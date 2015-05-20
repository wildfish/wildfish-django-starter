from rest_framework import serializers, viewsets
from {{cookiecutter.project_name}}.{{cookiecutter.app_name}}.models import {{cookiecutter.model_name}}


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = {{cookiecutter.model_name}}
        fields = (
            "id",
            "name",
        )


class ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = {{cookiecutter.model_name}}.objects.all()
    serializer_class = Serializer
    filter_fields = serializer_class.Meta.fields
