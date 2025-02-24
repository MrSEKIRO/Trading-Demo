from celery import shared_task

from .exchange import buy_from_exchange
from .models import Order

@shared_task
def process_order(order_id):
    pass
