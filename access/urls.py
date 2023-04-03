from django.urls import path

from . import views

urlpatterns = [
    path("login", views.loginv, name="login"),
    path("logout", views.logoutv, name="logout")
]
