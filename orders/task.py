from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import CartModel

@shared_task
def expire_carts():
    expiration_time = timezone.now() - timedelta(minutes=30)
    expired_carts = CartModel.objects.filter(
        updated_at__lte=expiration_time,
        is_expired=False
    )
    expired_carts.update(is_expired=True)
