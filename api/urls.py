from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views
from accounts.views import log_in, log_out

router = DefaultRouter()

router.register("clients", views.ClientViewSet, basename="client")
router.register("contracts", views.ContractViewSet, basename="contract")
router.register("events", views.EventViewSet, basename="event")

urlpatterns = [

    path("api-auth/login/", log_in),
    path("api-auth/logout/", log_out),
    path("api-auth/", include("rest_framework.urls")),

    path("", include(router.urls)),
    path("contracts/<int:contract_id>/sign/", views.sign_contract),

]
