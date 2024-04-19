import freezegun
import pytest

from orders.infrastructure.models.order import OrderProduct
from orders.infrastructure.serializers.order_serializer import OrderProductSerializer, OrderSerializer
from orders.infrastructure.serializers.product_serializer import ProductSerializer
from orders.infrastructure.models import Order, Product


@pytest.mark.django_db
@freezegun.freeze_time('2024-01-01')
def test_serialize_order_without_products():
    Order(
        total_price_without_taxes=20,
        total_price_with_taxes=30
    ).save()

    result = OrderSerializer(
        Order.objects.first()
    ).data
    del result['id']

    expected_result = {
        'articles': [],
        'total_price_without_taxes': '20.00',
        'total_price_with_taxes': '30.00',
        'created_at': '2024-01-01T00:00:00Z'
    }

    assert result == expected_result


@pytest.mark.django_db
@freezegun.freeze_time('2024-01-01')
def test_serialize_product():
    Product(
        reference='product_1',
        name='Product 1',
        description='Description of product 1',
        price_without_taxes=10,
        price_with_taxes=20,
    ).save()

    result = ProductSerializer(
        Product.objects.first()
    ).data
    del result['id']

    expected_result = {
        'reference': 'product_1',
        'name': 'Product 1',
        'description': 'Description of product 1',
        'price_without_taxes': '10.00',
        'price_with_taxes': '20.00',
        'created_at': '2024-01-01T00:00:00Z'
    }

    assert result == expected_result


@pytest.mark.django_db
@freezegun.freeze_time('2024-01-01')
def test_serialize_order_with_products():
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

    result = OrderSerializer(
        Order.objects.first()
    ).data
    del result['id']

    expected_result = {
        'articles': [{'quantity': 50, 'reference': 'product_1'}],
        'total_price_without_taxes': '20.00',
        'total_price_with_taxes': '30.00',
        'created_at': '2024-01-01T00:00:00Z'
    }

    assert result == expected_result
