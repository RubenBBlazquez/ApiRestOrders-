import cattrs

from orders.domain.entities.order import OrderDomain, OrderProductElement
from orders.domain.entities.order_product import OrderProductDomain
import pytest

from orders.domain.entities.product import ProductDomain


def test_order_product_domain():
    order_product_domain = OrderProductDomain.from_config(
        {
            'reference': 'product_1',
            'order_id': 1,
            'quantity': 10
        }
    )

    assert order_product_domain.parameters() == {
        'reference': 'product_1',
        'order_id': 1,
        'quantity': 10
    }


def test_order_product_domain_validation_error():
    with pytest.raises(cattrs.errors.ClassValidationError):
        OrderProductDomain.from_config(
            {
                'order_id': 1,
                'quantity': 10
            }
        )


def test_product_domain():
    product_domain = ProductDomain.from_config(
        {
            'reference': 'product_1',
            'name': 'Product 1',
            'description': 'Description of product 1',
            'price_without_taxes': 10,
            'taxes': 10
        }
    )

    assert product_domain.parameters() == {
        'reference': 'product_1',
        'name': 'Product 1',
        'description': 'Description of product 1',
        'price_without_taxes': 10,
        'taxes': 10
    }


def test_product_domain_validation_error():
    with pytest.raises(cattrs.errors.ClassValidationError):
        ProductDomain.from_config(
            {
                'reference': 'product_1',
                'name': 'Product 1',
                'description': 'Description of product 1',
                'price_without_taxes': 10,
            }
        )


def test_order_domain():
    order_domain = OrderDomain.from_config(
        {
            'products': [
                {
                    'reference': 'product_1',
                    'quantity': 10,
                    'product_price_without_taxes': 10,
                    'product_taxes': 10
                },
                {
                    'reference': 'product_2',
                    'quantity': 10,
                    'product_price_without_taxes': 10,
                    'product_taxes': 10
                }
            ],
            'total_price_without_taxes': 200,
            'total_price_with_taxes': 200
        }
    )

    assert order_domain.parameters() == {
        'products': [
            {
                'reference': 'product_1',
                'quantity': 10,
                'product_price_without_taxes': 10,
                'product_taxes': 10
            },
            {
                'reference': 'product_2',
                'quantity': 10,
                'product_price_without_taxes': 10,
                'product_taxes': 10
            }
        ],
        'total_price_without_taxes': 200,
        'total_price_with_taxes': 200
    }


@pytest.mark.parametrize(
    'fields',
    [
        {
            # with product without quantity
            'products': [
                {
                    'reference': 'product_1',
                    'product_taxes': 10,
                    'product_price_without_taxes': 10,
                },
                {
                    'reference': 'product_2',
                    'quantity': 10,
                    'product_price_without_taxes': 10,
                    'product_taxes': 10
                }
            ],
            'total_price_without_taxes': 200,
            'total_price_with_taxes': 200
        },
        # with product without reference
        {
            'products': [
                {
                    'quantity': 10,
                    'product_price_without_taxes': 10,
                    'product_taxes': 10
                },
                {
                    'reference': 'product_2',
                    'quantity': 10,
                    'product_price_without_taxes': 10,
                    'product_taxes': 10
                }
            ],
            'total_price_with_taxes': 200
        },
    ]

)
def test_order_domain_validation_error(fields):
    with pytest.raises(cattrs.errors.ClassValidationError):
        OrderDomain.from_config(fields)


def test_order_domain_add_product():
    order_domain = OrderDomain(
        products=[
            OrderProductElement(
                reference='product_1',
                quantity=10,
            ),
            OrderProductElement(
                reference='product_2',
                quantity=10,
            )
        ],
        total_price_without_taxes=200,
        total_price_with_taxes=200
    )

    order_domain.add_product(
        OrderProductElement(
            reference='product_3',
            quantity=10,
            product_price_without_taxes=10,
            product_taxes=10
        )
    )

    assert order_domain.products == [
        OrderProductElement(
            reference='product_1',
            quantity=10,
        ),
        OrderProductElement(
            reference='product_2',
            quantity=10,
        ),
        OrderProductElement(
            reference='product_3',
            quantity=10,
            product_price_without_taxes=10,
            product_taxes=10
        )
    ]


def test_update_total_price_without_taxes():
    order_domain = OrderDomain(
        products=[
            OrderProductElement(
                reference='product_1',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            ),
            OrderProductElement(
                reference='product_2',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            )
        ],
        total_price_without_taxes=0,
        total_price_with_taxes=0
    )

    order_domain.update_total_price_without_taxes()

    assert order_domain.total_price_without_taxes == 200


def test_update_total_price_with_taxes():
    order_domain = OrderDomain(
        products=[
            OrderProductElement(
                reference='product_1',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            ),
            OrderProductElement(
                reference='product_2',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            )
        ],
        total_price_without_taxes=0,
        total_price_with_taxes=0
    )

    order_domain.update_total_price_with_taxes()

    assert order_domain.total_price_with_taxes == 400

def test_set_products_to_edit():
    order_domain = OrderDomain(
        products=[
            OrderProductElement(
                reference='product_1',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            ),
            OrderProductElement(
                reference='product_2',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            )
        ],
        total_price_without_taxes=0,
        total_price_with_taxes=0

    )
    new_products = [
        OrderProductElement(
            reference='product_1',
            quantity=50
        ),
        OrderProductElement(
            reference='product_3',
            quantity=20
        )
    ]

    products_to_edit = []
    order_domain._set_products_to_edit(new_products, products_to_edit)

    assert products_to_edit == [
        OrderProductElement(
            reference='product_1',
            quantity=50,
            product_price_without_taxes=10,
            product_taxes=10
        )
    ]

def test_set_products_to_remove():
    order_domain = OrderDomain(
        products=[
            OrderProductElement(
                reference='product_1',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            ),
            OrderProductElement(
                reference='product_2',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            )
        ],
        total_price_without_taxes=0,
        total_price_with_taxes=0

    )
    new_products_references = ['product_1', 'product_3']

    products_to_remove = []
    order_domain._set_products_to_remove(new_products_references, products_to_remove)

    assert products_to_remove == [
        OrderProductElement(
            reference='product_2',
            quantity=10,
            product_price_without_taxes=10,
            product_taxes=10
        )
    ]

def test_get_products_to_check_existence():
    order_domain = OrderDomain(
        products=[
            OrderProductElement(
                reference='product_1',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            ),
            OrderProductElement(
                reference='product_2',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            )
        ],
        total_price_without_taxes=0,
        total_price_with_taxes=0

    )
    new_products = [
        OrderProductElement(
            reference='product_1',
            quantity=50
        ),
        OrderProductElement(
            reference='product_3',
            quantity=20
        )
    ]

    new_products_to_check_existence = order_domain._get_products_to_check_existence(new_products)

    assert new_products_to_check_existence == [
        OrderProductElement(
            reference='product_3',
            quantity=20
        )
    ]

def test_sync_order_with_new_products():
    order_domain = OrderDomain(
        products=[
            OrderProductElement(
                reference='product_1',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            ),
            OrderProductElement(
                reference='product_2',
                quantity=10,
                product_price_without_taxes=10,
                product_taxes=10
            )
        ],
        total_price_without_taxes=0,
        total_price_with_taxes=0

    )
    new_products = [
        OrderProductElement(
            reference='product_1',
            quantity=50
        ),
        OrderProductElement(
            reference='product_3',
            quantity=20
        )
    ]

    new_products_to_check_existence, products_to_remove, products_to_edit = order_domain.sync_order_with_new_products(new_products)

    assert new_products_to_check_existence == [
        OrderProductElement(
            reference='product_3',
            quantity=20
        )
    ]
    assert products_to_remove == [
        OrderProductElement(
            reference='product_2',
            quantity=10,
            product_price_without_taxes=10,
            product_taxes=10
        )
    ]
    assert products_to_edit == [
        OrderProductElement(
            reference='product_1',
            quantity=50,
            product_price_without_taxes=10,
            product_taxes=10
        )
    ]