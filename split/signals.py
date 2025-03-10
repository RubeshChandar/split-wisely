from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.db import transaction
post_expense_save = post_save


@receiver(post_expense_save, sender=Expense)
def create_splits(sender, instance, **kwargs):
    if kwargs.get("split_created"):
        splits = kwargs.get("splits")

        if splits:
            splits_to_create = []
            for user, amount in splits.items():
                temp = Split(user=user, expense=instance, amount=amount)
                splits_to_create.append(temp)

            if splits_to_create:
                with transaction.atomic():
                    Split.objects.bulk_create(splits_to_create)
