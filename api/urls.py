from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views

router = DefaultRouter()

router.register("clients", views.ClientViewSet, basename="client")
router.register("contracts", views.ContractViewSet, basename="contract")
router.register("events", views.EventViewSet, basename="event")

urlpatterns = [

    path("api-auth/", include("rest_framework.urls")),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),

    path("", include(router.urls)),
    path("contracts/<int:contract_id>/sign/", views.sign_contract),

]
