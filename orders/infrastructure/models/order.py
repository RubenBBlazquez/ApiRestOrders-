from django.db import models

from orders.infrastructure.models import Product


class OrderProduct(models.Model):
    """
    Model that represents the relationship between a product and an order.
    """
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    """
    Model that represents an order of products.
    """
    id = models.AutoField(primary_key=True)
    articles = models.ManyToManyField(Product, through='OrderProduct')
    total_price_without_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    total_price_with_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
