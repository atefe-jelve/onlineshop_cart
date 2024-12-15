from django.contrib import admin
from .models import CartModel, CartItems

admin.site.register(CartModel)
admin.site.register(CartItems)
