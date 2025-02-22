from django.db import models
from users.models import CustomUser


class Group(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(CustomUser, related_name="enrolledgroups")
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(default="", db_index=True, null=False)

    def __str__(self):
        return self.name


class GroupBalance(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="groupbalances")
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} -> {self.group} : {self.balance}"

    class Meta:
        unique_together = ('user', 'group')
        verbose_name = ("Group Balance")


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    paid_by = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="paid_expenses")
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="created_expenses")
