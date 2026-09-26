from django.shortcuts import render
import json
from django.db.models import F
import os
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Product
from .models import CartItem
def product_list_api(request):
   
    all_products = Product.objects.all()
    
    product_data = []
    for product in all_products:
        product_data.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
            'img': product.img.url if product.img else '' 
        })
        
    return JsonResponse(product_data, safe=False)

@csrf_exempt
@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        session_id = data.get('session_id')
        
        if not product_id or not session_id:
            return JsonResponse({"error": "Missing product_id or session_id"}, status=400)

        cart_item, created = CartItem.objects.get_or_create(
            session_id=session_id, 
            product_id=product_id,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity = F('quantity') + 1
            cart_item.save()
            
        return JsonResponse({"message": "Product added to cart successfully!"}, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
  

def get_cart_products(request):
    session_id = request.GET.get('session_id')
    
    if not session_id:
        return JsonResponse({"error": "Missing session_id"}, status=400)
        
    items = CartItem.objects.filter(session_id=session_id).select_related('product')
    
    cart_list = []
    for item in items:
        image_url = item.product.img.url if item.product.img else None
        cart_list.append({
            "id": item.id,                
            "product_id": item.product.id,
            "name": item.product.name,        
            "price": str(item.product.price), 
            "quantity": item.quantity,
            "image_url": image_url
        })
        
    return JsonResponse(cart_list, safe=False, status=200)

