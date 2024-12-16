from django.contrib import admin
from .models import CartModel, CartItems

admin.site.register(CartItems)


@admin.register(CartModel)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'is_expired', 'created_at')
    list_filter = ('is_expired', 'created_at')
    search_fields = ('user__username',)