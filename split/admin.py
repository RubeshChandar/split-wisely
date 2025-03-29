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
    list_display = ("user", "group", "balance", "modified")
    readonly_fields = ("modified", "created_at")
    list_filter = ("group", "modified")


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("description", "paid_by",
                    "amount",  "group")
    readonly_fields = ("created_at", "modified")
    list_filter = ("group",)
    search_fields = ("group__name", "description")


class SplitAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "get_expense_readable")
    readonly_fields = ("created_at", "modified")

    def get_expense_readable(self, obj):
        return format_html(f"<b> £{obj.expense.amount}</b> | {obj.expense.description}")

    get_expense_readable.short_description = "Expense"


class SettleAdmin(admin.ModelAdmin):
    list_display = ("group", "paid_by", "paid_to", "amount", "created_at")
    readonly_fields = ("created_at", "modified")


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupBalance, GroupBalanceAdmin)
admin.site.register(Split, SplitAdmin)
admin.site.register(Settlement, SettleAdmin)
admin.site.register(Expense, ExpenseAdmin)
