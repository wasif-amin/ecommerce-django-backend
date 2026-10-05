from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product

User = get_user_model()

# ==========================================
# 📦 BASIC MODEL & VIEW TESTS (Your Originals)
# ==========================================
class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Wireless Mouse",
            price=29.99,
            stock=10
        )

    def test_product_creation(self):
        """Verify that a product is created correctly with its fields."""
        self.assertEqual(self.product.name, "Wireless Mouse")
        self.assertEqual(self.product.price, 29.99)
        self.assertEqual(self.product.stock, 10)

    def test_product_string_representation(self):
        """Verify that the __str__ method returns the product name."""
        self.assertEqual(str(self.product), "Wireless Mouse")


class ProductViewTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Gaming Keyboard",
            price=89.99,
            stock=5
        )

    def test_product_list_view(self):
        """Verify the product catalog page loads successfully."""
        response = self.client.get(reverse('product_list_api')) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gaming Keyboard")


# ==========================================
# 🛒 PORTFOLIO-GRADE CART API TESTS (Fixed)
# ==========================================
class ProfessionalCartAPITests(APITestCase):
    def setUp(self):
        # 1. Create a test product
        self.product = Product.objects.create(
            name="Mechanical Keyboard",
            price=99.99,
            stock=5
        )
        
        # 2. Cache the URL from urls.py
        self.add_url = reverse('add_to_cart')
        
        # 3. Define a mock session ID for tracking the cart
        self.test_session_id = "mock-session-123xyz"

    def test_add_to_cart_success(self):
        """Success Path: Item is added to cart successfully when valid data is sent."""
        data = {
            "product_id": self.product.id, 
            "session_id": self.test_session_id
        }
        # Use format='json' to ensure it sends as raw JSON request.body
        response = self.client.post(self.add_url, data, format='json')
        
        # Matches your view's status=201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Product added to cart successfully!", response.json().get("message", ""))

    def test_add_to_cart_missing_parameters(self):
        """Validation: Missing fields return a 400 Bad Request error."""
        # Scenario A: Missing session_id
        data_missing_session = {"product_id": self.product.id}
        response = self.client.post(self.add_url, data_missing_session, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing product_id or session_id", response.json().get("error", ""))

        # Scenario B: Missing product_id
        data_missing_product = {"session_id": self.test_session_id}
        response = self.client.post(self.add_url, data_missing_product, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
