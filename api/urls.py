from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views
from accounts.views import log_in, log_out

router = DefaultRouter()

router.register("clients", views.ClientViewSet, basename="client")

urlpatterns = [

    # Authentication
    path("api-auth/login/", log_in),
    path("api-auth/logout/", log_out),
    path("api-auth/", include("rest_framework.urls")),

    path("", include(router.urls)),

]
