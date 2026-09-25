from django.db import models
from django.db import models
from cloudinary.models import CloudinaryField

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    img = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    session_id = models.CharField(max_length=255, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"