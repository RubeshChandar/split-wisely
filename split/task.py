from celery import shared_task
import time
import logging

logger = logging.getLogger(__name__)


@shared_task(name="update_group_balance")
def update_gb():
    return "Updated the balance"
