from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import normalizer

lowercase = normalizer("lowercase_normalizer", filter=["lowercase"])

import db.models as db

if settings.ES_DISABLE:
    decorator = lambda x: x
else:
    INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

    # See Elasticsearch Indices API reference for available settings
    INDEX.settings(number_of_shards=1, number_of_replicas=1)

    decorator = INDEX.doc_type


@decorator
class PlanningAppDocument(Document):
    """Declaration ElasticSearch doc"""

    # For CSV export keep these field names in sync with db/models

    db_id = fields.IntegerField(attr="id")

    description = fields.TextField(attr="description")

    area_name = fields.KeywordField(attr="area_name")
    near = fields.KeywordField(attr="near")
    decision = fields.KeywordField(attr="decision")
    app_type = fields.KeywordField(attr="app_type")

    location_x = fields.FloatField(attr="location_x")
    location_y = fields.FloatField(attr="location_y")

    date_received = fields.DateField(attr="date_received")

    description_key_lower = fields.KeywordField(
        attr="description", normalizer=lowercase
    )

    class Django(object):
        model = db.PlaningApp
