"""epic_events_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from accounts.admin import gestion_admin_site
from django.urls import path, include

from accounts import views

urlpatterns = [

    path("admin/logout/", views.log_out),
    path("admin/", admin.site.urls),

    path("gestion-admin/logout/", views.log_out),
    path("gestion-admin/", gestion_admin_site.urls),

    path("", include("accounts.urls")),
    path("", include("events.urls")),

]
