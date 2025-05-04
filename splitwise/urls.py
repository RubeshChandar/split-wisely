from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def forbidden(request):
    return render(request, "forbidden.html")


urlpatterns = [
    path("", include("split.urls")),
    path("admin/", admin.site.urls),
    path("user/", include("users.urls")),
    path("forbidden/", forbidden),
]
