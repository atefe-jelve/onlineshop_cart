
# celery -A onlineshop worker --beat --scheduler django --loglevel=info

from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.contrib.sessions.models import Session
from products.models import Product
from users.models import BaseUser
from .models import CartModel, CartItems
from .cart import CART_SESSION_ID


@shared_task
def check_expired_carts_task():
    sessions = Session.objects.all()
    expiration_time =  timedelta(minutes=3)

    for session in sessions:
        session_data = session.get_decoded()
        cart = session_data.get(CART_SESSION_ID)
        updated_at = session_data.get('updated_at')
        user_id = session_data.get('user')
        if cart:
            if updated_at:
                updated_at = datetime.fromisoformat(updated_at)
                if now() - updated_at > expiration_time:

                    save_cart_to_db(cart, user_id)
                    return_cart_quantities_to_stock(cart)
                    session.delete()

def save_cart_to_db(cart, user_id):
    """
    Save the expired cart to the database.
    """

    for product_id, item in cart.items():
        user = BaseUser.objects.get(id=user_id)
        card = CartModel.objects.create(
            user=user,
            total_price=int(item['price']) * item['quantity'],
            is_expired=True,
        )

        product = Product.objects.get(id=product_id)
        CartItems(card, product, item['quantity'])


def return_cart_quantities_to_stock(cart):
    """
    Return quantities in the expired cart to the product stock.
    """
    print('return to data base')
    for product_id, item in cart.items():

        product = Product.objects.get(id=product_id)
        product.inventory += item['quantity']
        product.save()
