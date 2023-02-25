from django.urls import path

from events import views

urlpatterns = [

    path("", views.about, name="about"),
    path("api/documentation/", views.api_doc, name="api_doc"),

]
