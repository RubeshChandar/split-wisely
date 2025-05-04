from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def forbidden(request):
    return render(request, "forbidden.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("split/", include("split.urls")),
    path("user/", include("users.urls")),
    path("forbidden/", forbidden),
]
