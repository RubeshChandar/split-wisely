from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.template.defaultfilters import slugify

from .models import *
from .tasks import *

post_expense_save = post_save


@receiver(post_save, sender=Group)
def make_a_slug(sender, instance, created, **kwargs):
    if created:
        slug = slugify(f"{instance.name} {instance.pk}")
        instance.slug = slug
        instance.save()


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

            update_gb.delay(instance.group_id)


@receiver(post_delete, sender=Expense)
def trigger_celery_update_gb(sender, instance, **kwargs):
    update_gb.delay(instance.group_id)


@receiver(m2m_changed, sender=Group.members.through)
def create_balance_for_new_group(sender, instance, action, **kwargs):
    if action in ('post_add', 'post_clear'):
        gbs_to_create = []
        user_pks = kwargs['pk_set']  # Get the set of user primary keys
        users = CustomUser.objects.filter(pk__in=user_pks)

        gb = GroupBalance.objects.filter(
            group=instance).values_list('user', flat=True)

        for user in users:
            if user.id not in gb:
                gbs_to_create.append(GroupBalance(
                    user=user, group=instance, balance=0))

        if gbs_to_create:
            with transaction.atomic():
                GroupBalance.objects.bulk_create(gbs_to_create)


@receiver([post_save, post_delete], sender=Settlement)
def trigger_celery_on_settlement_model(sender, instance, **kwargs):
    update_gb.delay(instance.group_id)
    print(f"Settlement Triggered on {instance.group_id}")
