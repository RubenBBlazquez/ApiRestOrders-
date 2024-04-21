from orders.application.use_cases.base import GetAllUseCase, GetByIdUseCase, CreateUseCase, EditUseCase
from unittest.mock import MagicMock, call, patch

from orders.application.use_cases.commands.base import DummyCommand, GetByIdCommand
from orders.application.use_cases.commands.create_order import CreateOrderCommand
from orders.application.use_cases.commands.create_product import CreateProductCommand
from orders.application.use_cases.commands.edit_order import EditOrderCommand
from orders.application.use_cases.commands.edit_product import EditProductCommand
from orders.application.use_cases.create_order import CreateOrderUseCase
from orders.application.use_cases.edit_order import EditOrderUseCase
from orders.domain.entities.order import OrderDomain, OrderProductElement
from orders.domain.entities.order_product import OrderProductDomain
from orders.domain.entities.product import ProductDomain
from orders.infrastructure.models import Product, Order


def test_get_all_use_case():
    repository_mock = MagicMock()
    command = DummyCommand()
    GetAllUseCase(repository=repository_mock).execute(command)
    repository_mock.get_all.assert_called_once()


def test_get_by_id_use_case():
    repository_mock = MagicMock()
    command = GetByIdCommand(
        identifier=1
    )
    GetByIdUseCase(repository=repository_mock).execute(command)
    repository_mock.get_by_id.assert_called_once_with(identifier=1)


def test_create_use_case():
    repository_mock = MagicMock()
    command = CreateProductCommand(
        reference='product_1',
        name='Product 1',
        description='Description of product 1',
        price_without_taxes=10,
        taxes=20
    )
    CreateUseCase(repository=repository_mock).execute(command)
    expected_entity = ProductDomain(
        reference='product_1',
        name='Product 1',
        description='Description of product 1',
        price_without_taxes=10.0,
        taxes=20.0
    )
    repository_mock.save.assert_called_once_with(entity=expected_entity)


def test_edit_use_case():
    repository_mock = MagicMock()
    command = EditProductCommand(
        identifier=1,
        reference='product_1',
        name='Product 1',
        description='Description of product 1',
        price_without_taxes=10,
        taxes=20
    )
    EditUseCase(repository=repository_mock).execute(command)
    expected_entity = ProductDomain(
        reference='product_1',
        name='Product 1',
        description='Description of product 1',
        price_without_taxes=10.0,
        taxes=20.0
    )

    repository_mock.update.assert_called_once_with(identifier=1, entity=expected_entity)


def test_create_order_use_case():
    order_repository_mock = MagicMock()
    order_repository_mock.save.return_value = Order(
        id=1,
        total_price_without_taxes=0,
        total_price_with_taxes=0
    )
    order_product_repository_mock = MagicMock()

    product_repository_mock = MagicMock()
    product_repository_mock.get_by_field.return_value.exists.return_value = True
    product_repository_mock.get_by_field.return_value.first.side_effect = [
        Product(
            reference='product_1',
            name='Product 1',
            description='Description of product 1',
            price_without_taxes=20,
            taxes=10
        ),
        Product(
            reference='product_2',
            name='Product 2',
            description='Description of product 2',
            price_without_taxes=20,
            taxes=10
        )
    ]

    command = CreateOrderCommand.from_config({
        "products": [
            {
                'reference': 'product_1',
                'quantity': 10,
            },
            {
                'reference': 'product_2',
                'quantity': 20,
            }
        ]
    })
    CreateOrderUseCase(
        order_repository=order_repository_mock,
        product_repository=product_repository_mock,
        order_product_repository=order_product_repository_mock
    ).execute(command)

    expected_order_domain = OrderDomain(
        products=[
            OrderProductElement(
                reference='product_1',
                quantity=10,
                product_price_without_taxes=20.0,
                product_taxes=10.0
            ),
            OrderProductElement(
                reference='product_2',
                quantity=20,
                product_price_without_taxes=20.0,
                product_taxes=10.0
            ),
        ],
        total_price_without_taxes=600.0,
        total_price_with_taxes=900.0,
    )
    expected_order_products_domain = [
        call(OrderProductDomain(
            reference='product_1',
            quantity=10,
            order_id=1
        )),
        call(OrderProductDomain(
            reference='product_2',
            quantity=20,
            order_id=1
        ))
    ]

    order_repository_mock.save.assert_called_once_with(expected_order_domain)
    order_product_repository_mock.save.assert_has_calls(expected_order_products_domain, any_order=True)


def test_edit_order_use_case():
    order_product_repository_mock = MagicMock()

    product_repository_mock = MagicMock()
    product_repository_mock.get_by_field.return_value.first.side_effect = [
        Product(
            reference='product_1',
            name='Product 1',
            description='Description of product 1',
            price_without_taxes=20,
            taxes=10
        ),
        Product(
            reference='product_2',
            name='Product 2',
            description='Description of product 2',
            price_without_taxes=20,
            taxes=10
        )
    ]

    command_mock = MagicMock()
    command_mock.products = [
        OrderProductElement(
            reference='product_1',
            quantity=10
        ),
        OrderProductElement(
            reference='product_2',
            quantity=20
        ),
        OrderProductElement(
            reference='product_4',
            quantity=60,
            product_price_without_taxes=20,
            product_taxes=10
        )
    ]

    order_repository_mock = MagicMock()
    order_repository_mock.get_by_id.return_value.to_domain.return_value.id = 1
    order_repository_mock.get_by_id.return_value.id = 1
    order_repository_mock.get_by_id.return_value.to_domain.return_value = OrderDomain(
        products=[
            OrderProductElement(
                reference='product_3',
                quantity=30
            ),
            OrderProductElement(
                reference='product_4',
                quantity=40
            )
        ],
        total_price_without_taxes=0,
        total_price_with_taxes=0
    )

    EditOrderUseCase(
        order_repository=order_repository_mock,
        product_repository=product_repository_mock,
        order_product_repository=order_product_repository_mock
    ).execute(command_mock)

    expected_save_order_product_calls = [
        call(
            OrderProductDomain(
                reference='product_1',
                quantity=10,
                order_id=1
            )
        ),
        call(
            OrderProductDomain(
                reference='product_2',
                quantity=20,
                order_id=1
            )
        ),
    ]
    expected_delete_order_products_calls = [
        call(
            OrderProductDomain(
                reference='product_3',
                quantity=30,
                order_id=1
            )
        ),
    ]
    expected_order_domain_update = OrderDomain(
            products=[
                OrderProductElement(
                    reference='product_4',
                    quantity=60,
                    product_price_without_taxes=0,
                    product_taxes=0),
                OrderProductElement(
                    reference='product_1',
                    quantity=10,
                    product_price_without_taxes=20.0,
                    product_taxes=10.0
                ),
                OrderProductElement(
                    reference='product_2',
                    quantity=20,
                    product_price_without_taxes=20.0,
                    product_taxes=10.0)
            ],
            total_price_without_taxes=600.0,
            total_price_with_taxes=900.0
        )

    order_product_repository_mock.save.assert_has_calls(expected_save_order_product_calls, any_order=True)
    order_product_repository_mock.delete.assert_has_calls(expected_delete_order_products_calls, any_order=True)
    order_repository_mock.update.assert_called_once_with(1, expected_order_domain_update)