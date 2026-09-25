from django.contrib import admin

# Register your models here.
from .models import Product, CartItem
admin.site.register(Product)
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'product', 'quantity') 