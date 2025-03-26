from django.db import connection, reset_queries, transaction
from celery import shared_task
import logging
from split.models import *
from django.core.cache import cache
from django.utils.timezone import now

logger = logging.getLogger(__name__)


@shared_task(name="update_group_balance")
def update_gb(group_id):
    reset_queries()

    try:
        group = Group.objects.get(pk=group_id)
        logger.info(f"Starting to make changes to the {group.name} group")

        # Prefetch the splits for all expenses and selected related to optimise
        # query perfomances and django calls those paid_by users with a extra query
        group_expenses = Expense.objects.filter(group=group)\
            .select_related("group", "paid_by")\
            .prefetch_related("splits__user")

        balance_sheet = {
            member: {'paid': 0, 'share': 0}
            for member in group.members.all()
        }

        # Updating the balance sheet
        for expense in group_expenses:
            balance_sheet[expense.paid_by]['paid'] += expense.amount
            for split in expense.splits.all():
                balance_sheet[split.user]['share'] += split.amount

        logger.info(f"Populated the balance sheet: {balance_sheet}")

        with transaction.atomic():
            group_balance = GroupBalance.objects.select_for_update()\
                .filter(group=group)

            logger.info(f"Group Balance row locked for update")

            gb = {g.user_id: g
                  for g in group_balance}

            balance_to_update = []
            balance_to_create = []

            for user, balance in balance_sheet.items():
                net_balance = balance['paid']-balance["share"]

                if user.id in gb:
                    gb[user.id].balance = net_balance
                    gb[user.id].modified = now()
                    balance_to_update.append(gb[user.id])

                else:
                    balance_to_create.append(GroupBalance(
                        user=user,
                        balance=net_balance,
                        group=group
                    ))

            if balance_to_update:

                logger.info(
                    f"There are {len(balance_to_update)} balance to be update")

                GroupBalance.objects.bulk_update(
                    balance_to_update, ['balance', 'modified'])

            if balance_to_create:
                logger.info(
                    f"There are {len(balance_to_create)} balance to be created")

                GroupBalance.objects.bulk_create(balance_to_create)

        logger.info(f"Group Balance row unlocked after update")
        logger.warning(f"Clearing the cache for group balance in {group.name}")
        cache_keyword = f"members-split-for-{group.slug}"
        cache.delete(cache_keyword)
        logger.info("Cache cleaned")

        return f"Changes made to {group.name} with {len(connection.queries)} queries"

    except:
        return f"Something went wrong"
