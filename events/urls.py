from django.urls import path

from events import views

urlpatterns = [

    path("", views.about, name="about"),
    path("api/documentation/", views.api_doc, name="api_doc"),
    path("clients/", views.client_list, name="client_list"),
    path("clients/nouveau/", views.client_create, name="client_create"),
    path("clients/<int:client_id>/", views.client_update, name="client_update"),
    path("clients/<int:client_id>/contrats/", views.contract_list, name="contract_list"),
]
