from .models import CartModel
from .cart import Cart
from celery import shared_task
from datetime import datetime, timedelta
import pytz

@shared_task
def remove_expire_carts(request):
    cart = Cart(request)
    expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=30)
    if cart['updated_at'] < expired_time:
        # session.pop(CART_SESSION_ID, None)
        expired_carts = CartModel.objects.filter(
            updated_at__lte=expired_time,
            is_expired=False
        )
        expired_carts.update(is_expired=True)

    # OtpCode.objects.filter(created__lt=expired_time).delete()

    # def save_to_database(self):
    #     """ Saves cart session to the database. """
    #     for product_id, item in self.cart.items():
    #         product = Product.objects.get(id=product_id)
    #         cart_model, created = CartModel.objects.create(
    #             user=self.session.get('user_id'),
    #             total_price=self.get_total_price(),
    #             is_expired=False,
    #         )
    #
    #         cart_model.quantity = item['quantity']
    #         cart_model.total_price = int(item['price']) * item['quantity']
    #         cart_model.save()