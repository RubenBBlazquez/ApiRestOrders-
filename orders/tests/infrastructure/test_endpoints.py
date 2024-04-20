import freezegun
import pytest

from django.urls import reverse
from django.test.client import Client

from orders.tests.conftest import create_test_product


@pytest.mark.django_db
@freezegun.freeze_time('2024-04-20')
def test_get_products_by_id():
    test_product = create_test_product()
    url = reverse("get_product_by_id")
    client = Client()
    response = client.get(f'{url}?id={test_product.pk}')
    result = response.json()

    assert result == {
        'id': test_product.pk,
        'reference': 'product_1',
        'name': 'Product 1',
        'description': 'Description of product 1',
        'price_without_taxes': '10.00',
        'taxes': '20.00',
        'created_at': '2024-04-20T00:00:00Z'
    }


@pytest.mark.django_db
@freezegun.freeze_time('2024-04-20')
def test_get_all_products():
    test_product = create_test_product()
    test_product2 = create_test_product()
    url = reverse("get_all_products")
    client = Client()
    response = client.get(url)
    result = response.json()

    assert result == [
        {
            'id': test_product.pk,
            'reference': 'product_1',
            'name': 'Product 1',
            'description': 'Description of product 1',
            'price_without_taxes': '10.00',
            'taxes': '20.00',
            'created_at': '2024-04-20T00:00:00Z'
        },
        {
            'id': test_product2.pk,
            'reference': 'product_1',
            'name': 'Product 1',
            'description': 'Description of product 1',
            'price_without_taxes': '10.00',
            'taxes': '20.00',
            'created_at': '2024-04-20T00:00:00Z'
        }
    ]


@pytest.mark.django_db
@freezegun.freeze_time('2024-04-20')
def test_create_product():
    body = {
        'reference': 'product_1',
        'name': 'Product 1',
        'description': 'Description of product 1',
        'price_without_taxes': 10,
        'taxes': 20
    }
    url = reverse("create_product")
    client = Client()
    response = client.post(url, data=body)
    result = response.json()
    del result['id']

    assert result == {
        'reference': 'product_1',
        'name': 'Product 1',
        'description': 'Description of product 1',
        'price_without_taxes': '10.00',
        'taxes': '20.00',
        'created_at': '2024-04-20T00:00:00Z'
    }
