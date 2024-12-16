from .models import BaseUser
from django.contrib import admin


@admin.register(BaseUser)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'is_active', 'is_admin')
    list_filter = ('username', 'phone_number')
    search_fields = ('username',)
