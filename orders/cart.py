from products.models import Product
from .models import CartModel
from django.utils import timezone
from datetime import timedelta

CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def save_to_database(self):
        """ Saves cart session to the database. """
        for product_id, item in self.cart.items():
            product = Product.objects.get(id=product_id)
            cart_model, created = CartModel.objects.get_or_create(
                user=self.session.get('user_id'),  # Assuming user_id is stored in session
                product=product,
                is_expired=False
            )
            cart_model.quantity = item['quantity']
            cart_model.total_price = int(item['price']) * item['quantity']
            cart_model.save()

    def expire_cart(self):
        """ Expire the cart after 30 minutes. """
        expiration_time = timezone.now() - timedelta(minutes=30)
        expired_carts = CartModel.objects.filter(
            updated_at__lte=expiration_time,
            is_expired=False
        )
        expired_carts.update(is_expired=True)
        # Remove cart session
        self.session.pop(CART_SESSION_ID, None)
