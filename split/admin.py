from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.


class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "modified", "created_by", "slug")

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


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("paid_by_name", "amount", "created_by_name", "group")
    readonly_fields = ("created_at", "modified")

    def paid_by_name(self, obj):
        return str(obj.paid_by.username).capitalize()

    def created_by_name(self, obj):
        return str(obj.created_by.username).capitalize()

    paid_by_name.short_description = "Paid by"
    created_by_name.short_description = "Created by"


class SplitAdmin(admin.ModelAdmin):
    list_display = ("get_username", "amount", "get_expense_readable")

    def get_username(self, obj):
        return str(obj.user.username).capitalize()

    def get_expense_readable(self, obj):
        return format_html(f"<b>ID : {obj.expense.id}</b> | {obj.expense}")

    get_username.short_description = "Username"
    get_expense_readable.short_description = "Expense"


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupBalance, GroupBalanceAdmin)
admin.site.register(Split, SplitAdmin)
admin.site.register(Expense, ExpenseAdmin)
