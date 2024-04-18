from django.db import models


class Product(models.Model):
    """
    Model that represents a product.
    """
    id = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_without_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    price_with_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
