from django.urls import path
from . import views

urlpatterns = [
    path("", views.signin, name="login"),
    path("register/", views.register, name="register"),
    path("check_username/", views.check_username, name='check-username'),
]
