from django.db import models

from orders.domain.entities.base import IDomainEntity
from orders.domain.entities.order import OrderDomain, OrderProductElement
from orders.domain.entities.order_product import OrderProductDomain
from orders.infrastructure.models import Product
from orders.infrastructure.models.base import ICustomModel


class OrderProduct(ICustomModel, models.Model):
    """
    Model that represents the relationship between a product and an order.
    """

    id = models.AutoField(primary_key=True)
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='order_products', on_delete=models.CASCADE)

    def to_domain(self) -> IDomainEntity:
        return OrderProductDomain(
            reference=self.product.reference,
            quantity=self.quantity,
            order_id=self.order.id
        )


class Order(ICustomModel, models.Model):
    """
    Model that represents an order of products.
    """
    id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(Product, through='OrderProduct')
    total_price_without_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    total_price_with_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_domain(self) -> IDomainEntity:
        return OrderDomain(
            products=[
                OrderProductElement(
                    reference=order_product.product.reference,
                    quantity=order_product.quantity,
                    product_price_without_taxes=float(order_product.product.price_without_taxes),
                    product_taxes=float(order_product.product.taxes)
                ) for order_product in self.order_products.all()
            ],
            total_price_without_taxes=float(self.total_price_without_taxes),
            total_price_with_taxes=float(self.total_price_with_taxes)
        )
