from django.urls import path

from events import views

urlpatterns = [

    path("", views.about, name="about"),

]
