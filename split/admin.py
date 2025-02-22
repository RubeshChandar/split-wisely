from django.contrib import admin
from .models import *
# Register your models here.


class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "modified", "created_by", )
    prepopulated_fields = {"slug": ("name",)}

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by when creating a new Group
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class GroupBalanceAdmin(admin.ModelAdmin):
    list_display = ("get_username", "user", "group", "balance")
    readonly_fields = ("modified",)

    def get_username(self, obj):
        return str(obj.user.username).capitalize()

    get_username.short_description = "Username"


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupBalance, GroupBalanceAdmin)
