from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.signin, name="login"),
    path("register/", views.register, name="register"),
    path("signout/", views.signout, name="signout"),
    path("check_username/", views.check_username, name='check-username'),
]
