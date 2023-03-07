from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views
from accounts.views import log_in, log_out

router = DefaultRouter()

router.register("clients", views.ClientViewSet, basename="client")
router.register("contracts", views.ContractViewSet, basename="contract")

urlpatterns = [

    path("", include(router.urls)),

    # Authentication
    path("api-auth/login/", log_in),
    path("api-auth/logout/", log_out),
    path("api-auth/", include("rest_framework.urls")),

    # Contract
    path("clients/<int:client_id>/contracts/", views.ContractCreate.as_view()),
    # path("/contracts/<int:contract_id>/sign/", ),

]
