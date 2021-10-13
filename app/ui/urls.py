from django.urls import path
from django.views.generic.base import TemplateView

from ui.views import CSVFromQueryDownloadView, DataView

app_name = "ui"

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("search", TemplateView.as_view(template_name="search.html"), name="search"),
    path("map-search", TemplateView.as_view(template_name="map_search.html"), name="map-search"),
    path("download_csv", CSVFromQueryDownloadView.as_view(), name="csv-download"),
]
