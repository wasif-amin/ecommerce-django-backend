from django.shortcuts import render
import json
from django.db.models import F
import os
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from rest_framework.decorators import api_view
import traceback
from rest_framework.response import Response
from rest_framework import status 
from .models import Product
from .models import CartItem
import stripe
from dotenv import load_dotenv 
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

@api_view(['PUT'])
def update_cart(request, item_id):
    try:
        change = request.data.get('change', 0)
        
        try:
            cart_item = CartItem.objects.get(pk=item_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if hasattr(cart_item.quantity, 'resolve_expression'):
            cart_item.refresh_from_db()

        cart_item.quantity += change
        
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
            
        return Response({"message": "Cart updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
        return Response({"success": "Item removed"}, status=status.HTTP_200_OK)
        
    except Cart.DoesNotExist:
        try:
            cart_item = Cart.objects.get(product_id=item_id)
            cart_item.delete()
            return Response({"success": "Item removed"}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response(
                {"error": f"Item with ID {item_id} not found as an ID or product_id"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Exception as e:
        return Response(
            {"error": "Internal server crash", "details": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@csrf_exempt
@require_POST
def checkout_session(request):
    try:
        load_dotenv()
        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
        
        data = json.loads(request.body)
        cart_items = data.get('items', [])
        
        
        line_items = []
        for item in cart_items:
            clean_price = str(item['price']).replace('$', '')
            
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['name'],
                    },
                    'unit_amount': int(float(clean_price) * 100),
                },
                'quantity': item['quantity'],
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:5173/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:5173/cart',
        )
        
        return JsonResponse({'url': checkout_session.url})
        
    except Exception as e:
        print("Stripe View Error:", str(e))
        return JsonResponse({'error': str(e)}, status=500)

