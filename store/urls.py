from django.urls import path
from .views import product_list_api, add_to_cart
from .views import product_list_api, add_to_cart, get_cart_products
urlpatterns = [
    path('products/', product_list_api, name='product_list_api'),
    path('add/cart/', add_to_cart, name='add_to_cart'),
    path('cart-products/', get_cart_products, name='get_cart_products')
]
