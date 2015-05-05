from haystack import indexes
from .models import {{cookiecutter.model_name}}


class {{cookiecutter.model_name}}Index(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return {{cookiecutter.model_name}}

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
