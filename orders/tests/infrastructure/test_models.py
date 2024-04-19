from datetime import datetime, timezone

import pytest

from orders.infrastructure.models import Product
from orders.infrastructure.models.order import Order, OrderProduct
import freezegun


@pytest.mark.django_db
@freezegun.freeze_time('2024-01-01')
def test_create_order_without_products():
    Order(
        total_price_without_taxes=20,
        total_price_with_taxes=30
    ).save()

    result = Order.objects.first()

    assert result.total_price_without_taxes == 20
    assert result.total_price_with_taxes == 30
    assert result.articles.count() == 0
    assert result.created_at == datetime(2024, 1, 1, tzinfo=timezone.utc)


@pytest.mark.django_db
@freezegun.freeze_time('2024-01-01')
def test_create_product():
    Product(
        reference='product_1',
        name='Product 1',
        description='Description of product 1',
        price_without_taxes=10,
        price_with_taxes=20,
    ).save()

    result = Product.objects.first()

    assert result.reference == 'product_1'
    assert result.name == 'Product 1'
    assert result.description == 'Description of product 1'
    assert result.price_without_taxes == 10
    assert result.price_with_taxes == 20
    assert result.created_at == datetime(2024, 1, 1, tzinfo=timezone.utc)

@pytest.mark.django_db
@freezegun.freeze_time('2024-01-01')
def test_create_order_with_product():
    product = Product(
        reference='product_1',
        name='Product 1',
        description='Description of product 1',
        price_without_taxes=10,
        price_with_taxes=20,
    )
    product.save()
    order = Order(
        total_price_without_taxes=20,
        total_price_with_taxes=30
    )
    order.save()
    OrderProduct(
        quantity=50,
        product=product,
        order=order
    ).save()

    result = Order.objects.first()
    assert result.order_products.first().quantity == 50
