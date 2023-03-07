from django.urls import path, include

from api import views
from accounts.views import log_in, log_out

urlpatterns = [

    # Authentication
    path("api-auth/login/", log_in),
    path("api-auth/logout/", log_out),
    path("api-auth/", include("rest_framework.urls")),

    # Clients
    path("clients/", views.ClientListCreate.as_view()),
    path("clients/<int:client_id>/", views.ClientRetrieveUpdate.as_view()),

    # Contracts
    path("clients/<int:client_id>/contracts/", views.ContractListCreate.as_view()),

]
