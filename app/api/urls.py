from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
import api.views

app_name = "api"

router = DefaultRouter()

router.register(r"PlanningApps", api.views.PlanningAppViewSet, basename="planning-apps")

urlpatterns = [
    path("datasets", api.views.DatasetsApiView.as_view(), name="datasets",),
    url(r"^", include(router.urls)),
]
