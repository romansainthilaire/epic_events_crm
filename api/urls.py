from django.urls import path, include

from api import views

urlpatterns = [

    # Authentication
    path("api-auth/", include("rest_framework.urls")),

    # Clients
    path("clients/", views.ClientList.as_view()),

]
