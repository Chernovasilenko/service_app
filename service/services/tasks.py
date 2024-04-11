import datetime

from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.db.models import F


HUNDRED_PERCENT = 100.0


@shared_task(base=Singleton)
def set_price(subscription_id):
    from services.models import Subscription

    with transaction.atomic():

        subscription = Subscription.objects.select_for_update().filter(
            id=subscription_id
        ).annotate(
            annotated_price=(
                F('service__full_price') *
                ((HUNDRED_PERCENT - F('plan__discount_percent')) /
                 HUNDRED_PERCENT)
            )
        ).first()

        subscription.price = subscription.annotated_price
        subscription.save()


@shared_task(base=Singleton)
def set_comment(subscription_id):
    from services.models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(
            id=subscription_id
        )

        subscription.comment = str(datetime.datetime.now())
        subscription.save()
