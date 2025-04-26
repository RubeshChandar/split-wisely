from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("<slug:slug>/", views.singleGroupView, name="single-group"),
    path("<slug:slug>/members-split", views.members_split, name="members_split"),
    path("<slug:slug>/add-expense/", views.add_expense, name="add_expense"),
]

htmx_urlpatterns = [
    path("<slug:slug>/settle/", views.SettlementView.as_view(), name="settle"),
    path("<slug:slug>/check-settlement/",
         views.check_settle_amount, name="check-settle"),
    path("settle/<int:pk>/delete/",
         views.delete_transaction, {'trans_type': 'settlement'}, name="delete-settlement"),
    path("expense/<int:pk>/delete/",
         views.delete_transaction, {'trans_type': 'expense'}, name="delete-expense"),
    path("expense/<int:pk>/view-shares/", views.get_shares, name="view-shares")
]


urlpatterns += htmx_urlpatterns
