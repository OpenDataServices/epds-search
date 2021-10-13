from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

import db.models as db
import elastic.documents as documents


class Dataset(serializers.ModelSerializer):
    class Meta:
        model = db.Dataset
        fields = "__all__"


class PlanningAppDocumentSerializer(DocumentSerializer):
    class Meta:
        document = documents.PlanningAppDocument
