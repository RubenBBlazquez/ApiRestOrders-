from django.db import models

from orders.infrastructure.models import Product


class OrderProduct(models.Model):
    """
    Model that represents the relationship between a product and an order.
    """
    id = models.AutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='order_products', on_delete=models.CASCADE)


class Order(models.Model):
    """
    Model that represents an order of products.
    """
    id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(Product, through='OrderProduct')
    total_price_without_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    total_price_with_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
