from django.contrib import admin
from .models import *
from django.utils.html import format_html


class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
    readonly_fields = ("created_at", "modified", "created_by", "slug", "id")

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by when creating a new Group
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class GroupBalanceAdmin(admin.ModelAdmin):
    list_display = ("get_username",
                    "group", "balance", "modified")
    readonly_fields = ("modified", "created_at")
    list_filter = ("group", "modified")

    def get_username(self, obj):
        return str(obj.user.username).capitalize()

    get_username.short_description = "Username"


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("description", "paid_by_name",
                    "amount", "created_by_name", "group")
    readonly_fields = ("created_at", "modified")
    list_filter = ("group",)
    search_fields = ("group__name", "description")

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
        return format_html(f"<b>{obj.expense.id}</b> | <b> £{obj.expense.amount}</b> | {obj.expense.description}")

    get_username.short_description = "Username"
    get_expense_readable.short_description = "Expense"


class SettleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupBalance, GroupBalanceAdmin)
admin.site.register(Split, SplitAdmin)
admin.site.register(Settlement, SettleAdmin)
admin.site.register(Expense, ExpenseAdmin)
