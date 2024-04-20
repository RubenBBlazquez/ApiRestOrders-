import pytest

from orders.infrastructure.models import Product, Order
from orders.infrastructure.models.order import OrderProduct


def create_test_product():
    product = Product(
        reference='product_1',
        name='Product 1',
        description='Description of product 1',
        price_without_taxes=10,
        taxes=20,
    )
    product.save()
    return product


def create_test_order():
    order = Order(
        total_price_without_taxes=20,
        total_price_with_taxes=30
    )
    order.save()
    return order


def create_test_order_product(order=None, product=None):
    if not product:
        product = create_test_product()
    if not order:
        order = create_test_order()

    order_product = OrderProduct(
        product=product,
        order=order,
        quantity=10
    )
    order_product.save()

    return order_product
