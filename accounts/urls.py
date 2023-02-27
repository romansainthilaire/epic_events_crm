from django.urls import path

from accounts import views

urlpatterns = [
    path("connexion/", views.log_in, name="login"),
    path("deconnexion/", views.log_out, name="logout"),
]
