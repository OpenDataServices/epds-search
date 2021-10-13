import django_filters.rest_framework
from rest_framework import filters, generics
from rest_framework.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FacetedSearchFilterBackend,
    CompoundSearchFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
)
from elasticsearch_dsl import TermsFacet, DateHistogramFacet, RangeFacet

import api.serializers as serializers
import db.models as db
import elastic.documents as elastic
from api.sized_faceted_search_backend import SizedFacetedSearchFilterBackend


# Direct database as api example
#
#
class DefaultPaginator(LimitOffsetPagination):
    default_limit = 60


class DatasetsApiView(generics.ListAPIView):
    serializer_class = serializers.Dataset
    pagination_class = DefaultPaginator

    filter_fields = ("id",)
    filter_backends = (
        filters.SearchFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    )

    def get_queryset(self):
        return db.Dataset.objects.all()


# Elasticsearch as api


class PlanningAppViewSet(DocumentViewSet):
    document = elastic.PlanningAppDocument
    serializer_class = serializers.PlanningAppDocumentSerializer

    filter_backends = (
        SizedFacetedSearchFilterBackend,
        CompoundSearchFilterBackend,
        FilteringFilterBackend,
        OrderingFilterBackend,
    )

    # CompoundSearchFilter ?search= , ?search=field:value
    search_fields = (
        "description_key_lower",
        "description",
        "area_name",
    )

    # FacetedSearchFilterBackend ?facet=name
    faceted_search_fields = {
        "decision": {
            "field": "decision",
            "facet": TermsFacet,
            "enabled": True,
        },
        "area_name": {
            "field": "area_name",
            "facet": TermsFacet,
            "enabled": True,
            "options": {"size": 50},
        },
        "near": {
            "field": "near",
            "facet": TermsFacet,
            "enabled": True,
            "options": {"size": 50},
        },
        "app_type": {
            "field": "app_type",
            "facet": TermsFacet,
            "enabled": True,
            "options": {"size": 50},
        },
        "date_received": {
            "field": "date_received",
            "facet": DateHistogramFacet,
            "options": {"interval": "year"},
            "enabled": True,
        },
    }

    # FilteringFilterBackend ?member_id=N
    filter_fields = {
        "near": "near",
        "area_name": "area_name",
        "date_received": "date_received",
        "db_id": "db_id",
        "app_type": "app_type",
        "decision": "decision",
        "description": "description_key_lower",
    }

    # OrderingFilterBackend ?ordering=fetched ascending descending ?ordering=-fetched
    ordering_fields = {
        "date_received": "date_received",
    }
