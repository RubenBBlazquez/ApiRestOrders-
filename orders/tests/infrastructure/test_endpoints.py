import json

import freezegun
import pytest

from django.urls import reverse
from django.test.client import Client

from orders.tests.conftest import create_test_product, create_test_order, create_test_order_product


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
    response = client.post(url, data=body, content_type='application/json')
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


@pytest.mark.django_db
@freezegun.freeze_time('2024-04-20')
def test_edit_product():
    test_product = create_test_product()
    body = {
        'identifier': test_product.pk,
        'reference': 'product_edited',
        'name': 'Product 1 edited',
        'description': 'Description of product 1 edited',
        'price_without_taxes': 25,
        'taxes': 35
    }
    url = reverse("edit_product")
    client = Client()
    response = client.put(url, data=body)
    result = response.json()
    del result['id']

    assert result == {
        'reference': 'product_edited',
        'name': 'Product 1 edited',
        'description': 'Description of product 1 edited',
        'price_without_taxes': '25.00',
        'taxes': '35.00',
        'created_at': '2024-04-20T00:00:00Z'
    }


@pytest.mark.django_db
@freezegun.freeze_time('2024-04-20')
def test_get_order_by_id():
    order = create_test_order()
    create_test_order_product(order)
    url = reverse("get_order_by_id")
    client = Client()
    response = client.get(f'{url}?id={order.pk}')
    result = response.json()
    del result['id']

    assert result == {
        'products': [{'quantity': 10, 'reference': 'product_1'}],
        'total_price_without_taxes': '20.00',
        'total_price_with_taxes': '30.00',
        'created_at': '2024-04-20T00:00:00Z'
    }


@pytest.mark.django_db
@freezegun.freeze_time('2024-04-20')
def test_get_all_orders():
    order = create_test_order()
    create_test_order_product(order)
    order2 = create_test_order()
    url = reverse("get_all_orders")
    client = Client()
    response = client.get(url)
    result = response.json()

    assert result == [
        {
            'id': order.id,
            'products': [{'quantity': 10, 'reference': 'product_1'}],
            'total_price_without_taxes': '20.00',
            'total_price_with_taxes': '30.00',
            'created_at': '2024-04-20T00:00:00Z'
        },
        {
            'id': order2.id,
            'products': [],
            'total_price_without_taxes': '20.00',
            'total_price_with_taxes': '30.00',
            'created_at': '2024-04-20T00:00:00Z'
        }
    ]


@pytest.mark.django_db
@freezegun.freeze_time('2024-04-20')
def test_create_order_with_valid_products():
    create_test_product('product_1')
    create_test_product('product_2')
    create_test_product('product_3')

    url = reverse("create_order")
    client = Client()
    response = client.post(url, data=json.dumps({
        'products': [
            {'reference': 'product_1', 'quantity': 10},
            {'reference': 'product_2', 'quantity': 10},
            {'reference': 'product_3', 'quantity': 10}
        ]
    }), content_type='application/json')

    result = response.json()
    del result['created_order']['id']

    assert result == {
        'created_order':
            {
                'products': [
                    {'quantity': 10, 'reference': 'product_1'},
                    {'quantity': 10, 'reference': 'product_2'},
                    {'quantity': 10, 'reference': 'product_3'}
                ],
                'total_price_without_taxes': '300.00',
                'total_price_with_taxes': '900.00',
                'created_at': '2024-04-20T00:00:00Z'
            },
        'not_valid_products': []
    }


@pytest.mark.django_db
@freezegun.freeze_time('2024-04-20')
def test_create_order_without_valid_products():
    url = reverse("create_order")
    client = Client()
    response = client.post(url, data=json.dumps({
        'products': [
            {'reference': 'product_1', 'quantity': 10},
            {'reference': 'product_2', 'quantity': 10},
            {'reference': 'product_3', 'quantity': 10}
        ]
    }), content_type='application/json')

    result = response.json()
    del result['created_order']['id']

    assert result == {
        'created_order':
            {
                'products': [],
                'total_price_without_taxes': '0.00',
                'total_price_with_taxes': '0.00',
                'created_at': '2024-04-20T00:00:00Z'
            },
        'not_valid_products': [
            'product_1',
            'product_2',
            'product_3'
        ]
    }
