from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Company, Exchange


@registry.register_document
class CompanyDocument(Document):
    exchange = fields.ObjectField(properties={
        'code': fields.TextField(),
        'currency': fields.TextField(),
        'name': fields.TextField(),
    })
    class Index:
        # Name of the Elasticsearch index
        name = 'company'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Company # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'description',
            'displaySymbol',
            'symbol',
            'id',
        ]
        related_models = [Exchange]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(CompanyDocument, self).get_queryset().select_related(
            'exchange'
        )