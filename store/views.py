from django.shortcuts import render

# your_app_name/views.py
from django.http import JsonResponse
from .models import Product

def product_list_api(request):
    # 1. Fetch the data
    all_products = Product.objects.all()
    
    # 2. Convert the database rows into a Python list of dictionaries
    product_data = list(all_products.values('id', 'name', 'price', 'stock', 'img'))
    print(product_data)
    # 3. Return the data as JSON
    return JsonResponse(product_data, safe=False)

