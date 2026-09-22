from django.shortcuts import render
import json
import os
from django.contrib.auth.hashers import check_password_hash
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
@csrf_exempt
def wasif_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            password = data.get("password")

            admin_hash = os.environ.get("ADMIN_PASSWORD_HASH")

            if admin_hash and check_password_hash(password, admin_hash):
                request.session["is_admin"] = True
                return JsonResponse({"message": "logged in!"}, status=200)
            return JsonResponse({"error": "Invalid password"}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)
