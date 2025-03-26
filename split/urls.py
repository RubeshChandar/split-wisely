from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("<slug:slug>/", views.singleGroupView, name="single-group"),
    path("<slug:slug>/members-split", views.members_split, name="members_split"),
    path("<slug:slug>/add-expense/", views.add_expense, name="add_expense"),
    path("<slug:slug>/settle/", views.settlement, name="settle"),
]
