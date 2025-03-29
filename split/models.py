from django.db import models
from django.urls import reverse
from users.models import CustomUser
from django.template.defaultfilters import slugify


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Group(TimeStampModel):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(CustomUser, related_name="enrolledgroups")
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="created_groups")
    slug = models.SlugField(default="", unique=True, db_index=True, null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("single-group", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name} {self.pk}")
        return super().save(*args, **kwargs)


class GroupBalance(TimeStampModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_group_balance")
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group_balances")

    def __str__(self):
        return f"{self.user.username} -> {self.group} : {self.balance}"

    class Meta:
        unique_together = ('user', 'group')
        verbose_name = ("Group Balance")
        verbose_name_plural = ("Group Balance")
        ordering = ["-modified", "-group__modified"]


class Expense(TimeStampModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    paid_by = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="paid_expenses")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group_expenses")
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="created_expenses")

    def __str__(self):
        return f"{self.group.name.capitalize()} -> {self.amount}"

    class Meta:
        ordering = ["-created_at"]


class Split(TimeStampModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense = models.ForeignKey(
        Expense, on_delete=models.CASCADE, related_name="splits")

    class Meta:
        unique_together = ("user", "expense")

    def __str__(self):
        return f"{self.user} -> {self.amount}"


class Settlement(TimeStampModel):
    paid_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="settle_pb")
    paid_to = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="settle_pt")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group_settlements")

    def __str__(self):
        return f"{self.paid_by} settled {self.amount} to {self.paid_to}"
