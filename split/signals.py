from django.db.models.signals import post_save, m2m_changed
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


@receiver(m2m_changed, sender=Group.members.through)
def create_balance_for_new_group(sender, instance, action, **kwargs):
    if action in ('post_add', 'post_clear'):
        gbs_to_create = []
        user_pks = kwargs['pk_set']  # Get the set of user primary keys
        users = CustomUser.objects.filter(pk__in=user_pks)

        for user in users:
            gbs_to_create.append(GroupBalance(
                user=user, group=instance, balance=0))

        if gbs_to_create:
            with transaction.atomic():
                GroupBalance.objects.bulk_create(gbs_to_create)
