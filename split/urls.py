from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("new-create-group/", views.create_grp, name="new-group"),
    path("<slug:slug>/delete-group/", views.delete_grp, name="delete-group"),
    path("<slug:slug>/", views.singleGroupView, name="single-group"),
    path("<slug:slug>/members-split/", views.members_split, name="members_split"),
    path("<slug:slug>/add-expense/", views.add_expense, name="add_expense"),
    path("<slug:slug>/manage-members/",
         views.manage_members, name="manage_members"),

]

htmx_urlpatterns = [
    path("<slug:slug>/settle/", views.SettlementView.as_view(), name="settle"),
    path("<slug:slug>/check-settlement/",
         views.check_settle_amount, name="check-settle"),
    path("settle/<int:pk>/delete/",
         views.delete_transaction, {'trans_type': 'settlement'}, name="delete-settlement"),
    path("expense/<int:pk>/delete/",
         views.delete_transaction, {'trans_type': 'expense'}, name="delete-expense"),
    path("expense/<int:pk>/view-shares/", views.get_shares, name="view-shares"),
    path("<slug:slug>/search-user/",
         views.search_user, name="search-user"),
    path("<slug:slug>/manage-members/add-member/<int:pk>",
         views.manage_members, {'action': 'add'}, name="add_member"),
    path("<slug:slug>/manage-members/remove-member/<int:pk>",
         views.manage_members, {'action': 'remove'}, name="remove_member"),

]


urlpatterns += htmx_urlpatterns
