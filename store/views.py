from django.shortcuts import render
import json
import os
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# your_app_name/views.py
from django.http import JsonResponse
from .models import Product

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