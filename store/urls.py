from django.urls import path
from .views import product_list_api, add_to_cart, get_cart_products, update_cart, remove_from_cart, checkout_session
from . import views
urlpatterns = [
    path('products/', product_list_api, name='product_list_api'),
    path('add/cart/', add_to_cart, name='add_to_cart'),
    path('cart-products/', get_cart_products, name='get_cart_products'),
    path('update-cart-item/<int:item_id>', update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove-from-cart'),
    path('checkout-session/', views.checkout_session, name='checkout_session'),

]
