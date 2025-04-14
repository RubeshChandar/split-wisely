import logging
import traceback
from django.utils.timezone import now
from collections import defaultdict
from django.core.cache import cache
from celery import shared_task
from django.db import connection, reset_queries, transaction
from django.db.models import Sum

from split.models import *

logger = logging.getLogger(__name__)


@shared_task(name="update_group_balance")
def update_gb(group_id):
    reset_queries()

    try:
        group = Group.objects.get(pk=group_id)
        logger.info(f"Starting to make changes to the {group.name} group")

        balance_sheet = defaultdict(
            lambda: {'paid': 0, 'in': 0, 'out': 0, 'share': 0}
        )

        # Getting the individuals fields needed to calculate the balance
        for row in Expense.objects.filter(group_id=group_id).values("paid_by").annotate(total=Sum("amount")):
            balance_sheet[row['paid_by']]['paid'] += row['total']

        for row in Split.objects.filter(expense__group_id=group_id).values("user").annotate(total=Sum("amount")):
            balance_sheet[row['user']]['share'] += row['total']

        for row in Settlement.objects.filter(group_id=group_id).values("paid_to").annotate(total=Sum("amount")):
            balance_sheet[row['paid_to']]['in'] += row['total']

        for row in Settlement.objects.filter(group_id=group_id).values("paid_by").annotate(total=Sum("amount")):
            balance_sheet[row['paid_by']]['out'] += row['total']

        # Much cleaner logic for calculating the group balance.
        final_balance = {
            user_id: round(values['paid'] - values['share'] +
                           values['out'] - values['in'], 2)
            for user_id, values in balance_sheet.items()
        }

        logger.info(f"Populated the balance sheet: {final_balance}")

        with transaction.atomic():
            group_balance = GroupBalance.objects.select_for_update()\
                .filter(group=group)

            logger.info(f"Group Balance row locked for update")

            gb = {g.user_id: g for g in group_balance}

            balance_to_create, balance_to_update = [], []

            for id, balance in final_balance.items():

                if id in gb:
                    gb[id].balance = balance
                    gb[id].modified = now()
                    balance_to_update.append(gb[id])

                else:
                    balance_to_create.append(
                        GroupBalance(
                            user_id=id,
                            balance=balance,
                            group_id=group_id
                        )
                    )

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

    except Exception as e:
        logger.error(
            f"Error updating group balance for group ID {group_id}: {e}")
        logger.debug("Stack Trace:\n" + traceback.format_exc())
        return f"Something went wrong: {e}"
