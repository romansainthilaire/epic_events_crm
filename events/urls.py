from django.urls import path

from events import views

urlpatterns = [

    path("", views.about, name="about"),
    path("api/documentation/", views.api_doc, name="api_doc"),

    # Client
    path("clients/", views.client_list, name="client_list"),
    path("clients/nouveau/", views.client_create, name="client_create"),
    path("clients/<int:client_id>/", views.client_update, name="client_update"),

    # Contract
    path("clients/<int:client_id>/contrats/", views.contract_list, name="contract_list"),
    path("clients/<int:client_id>/contrats/nouveau/", views.contract_create, name="contract_create"),
    path("contrats/<int:contract_id>/", views.contract_update, name="contract_update"),
    path("contrats/<int:contract_id>/supprimer/", views.contract_delete, name="contract_delete"),
    path("contrats/<int:contract_id>/signer/", views.contract_sign, name="contract_sign"),

]
