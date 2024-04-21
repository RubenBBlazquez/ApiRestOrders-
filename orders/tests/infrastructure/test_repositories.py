import freezegun
import pytest

from orders.domain.entities.order import OrderDomain
from orders.domain.entities.product import ProductDomain
from orders.infrastructure.repositories.order_repository import OrderRepository
from orders.infrastructure.repositories.product_repository import ProductRepository
from orders.infrastructure.serializers.order_serializer import OrderSerializer
from orders.infrastructure.serializers.product_serializer import ProductSerializer
from orders.tests.conftest import create_test_product, create_test_order


@pytest.mark.django_db
def test_get_by_id_product():
    product = create_test_product()
    repository = ProductRepository()
    result = repository.get_by_id(product.id)

    assert result.id == product.id


@pytest.mark.django_db
def test_get_all_product():
    product = create_test_product()
    product2 = create_test_product()
    repository = ProductRepository()
    result = repository.get_all()

    assert len(result) == 2
    assert result[0].id == product.id
    assert result[1].id == product2.id


@pytest.mark.django_db
@freezegun.freeze_time('2024-01-01')
def test_save_product():
    product_domain = ProductDomain(
        reference='product_save',
        name='Product 1 save',
        description='Description of product 1 save',
        price_without_taxes=10,
        taxes=20,
    )
    repository = ProductRepository()
    product = repository.save(product_domain)
    result = ProductSerializer(product).data
    del result['id']

    assert result == {
        'reference': 'product_save',
        'name': 'Product 1 save',
        'description': 'Description of product 1 save',
        'price_without_taxes': '10.00',
        'taxes': '20.00',
        'created_at': '2024-01-01T00:00:00Z'
    }


@pytest.mark.django_db
@freezegun.freeze_time('2024-01-01')
def test_edit_product():
    product = create_test_product()
    product_domain = ProductDomain(
        reference='product_edit',
        name='Product 1 edit',
        description='Description of product 1 edit',
        price_without_taxes=10,
        taxes=20,
    )
    repository = ProductRepository()
    product = repository.update(product.id, product_domain)
    result = ProductSerializer(product).data
    del result['id']

    assert result == {
        'reference': 'product_edit',
        'name': 'Product 1 edit',
        'description': 'Description of product 1 edit',
        'price_without_taxes': '10.00',
        'taxes': '20.00',
        'created_at': '2024-01-01T00:00:00Z'
    }


@pytest.mark.django_db
def test_get_by_id_order():
    order = create_test_order()
    repository = OrderRepository()
    result = repository.get_by_id(order.id)

    assert result.id == order.id


@pytest.mark.django_db
def test_get_all_orders():
    order = create_test_order()
    order2 = create_test_order()
    repository = OrderRepository()
    result = repository.get_all()

    assert len(result) == 2
    assert result[0].id == order.id
    assert result[1].id == order2.id


@pytest.mark.django_db
@freezegun.freeze_time('2024-01-01')
def test_save_order():
    order_domain = OrderDomain(
        products=[],
        total_price_without_taxes=20,
        total_price_with_taxes=30
    )
    repository = OrderRepository()
    order = repository.save(order_domain)
    result = OrderSerializer(order).data
    del result['id']

    assert result == {
        'products': [],
        'total_price_without_taxes': '20.00',
        'total_price_with_taxes': '30.00',
        'created_at': '2024-01-01T00:00:00Z'
    }


@pytest.mark.django_db
@freezegun.freeze_time('2024-01-01')
def test_edit_order():
    order = create_test_order()
    order_domain = OrderDomain(
        products=[],
        total_price_without_taxes=50,
        total_price_with_taxes=60
    )
    repository = OrderRepository()
    product = repository.update(order.id, order_domain)
    result = OrderSerializer(product).data
    del result['id']

    assert result == {
        'products': [],
        'total_price_without_taxes': '50.00',
        'total_price_with_taxes': '60.00',
        'created_at': '2024-01-01T00:00:00Z'
    }
