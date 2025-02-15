from django.contrib import admin
from .models import *
# Register your models here.


class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "modified", "created_by",)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by when creating a new Group
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Group, GroupAdmin)
