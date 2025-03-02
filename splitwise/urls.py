
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("split/", include("split.urls")),
    path("user/", include("users.urls")),
    path("__debug__/", include("debug_toolbar.urls"))
]
