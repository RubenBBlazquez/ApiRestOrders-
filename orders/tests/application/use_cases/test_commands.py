from orders.application.use_cases.commands.base import GetByIdCommand
import pytest

from orders.application.use_cases.commands.create_product import CreateProductCommand
from orders.application.use_cases.commands.edit_product import EditProductCommand
from orders.domain.entities.product import ProductDomain
import cattrs


def test_get_by_id_command_ok():
    command = GetByIdCommand.from_config({
        'identifier': '1'
    })
    assert command.data() == {
        'identifier': '1'
    }


def test_get_by_id_command_identifier_not_found():
    with pytest.raises(KeyError):
        GetByIdCommand.from_config({})


def test_create_product_command():
    command = CreateProductCommand.from_config(
        {
            'reference': 'product_1',
            'name': 'Product 1',
            'description': 'Description of product 1',
            'price_without_taxes': 10,
            'taxes': 20
        }
    )
    result = command.data()

    assert result == {
        'entity': ProductDomain.from_config(
            {
                'reference': 'product_1',
                'name': 'Product 1',
                'description': 'Description of product 1',
                'price_without_taxes': 10,
                'taxes': 20
            }
        )
    }


@pytest.mark.parametrize(
    'fields',
    [
        {
            'reference': 'product_1',
            'description': 'Description of product 1',
            'price_without_taxes': 10,
            'taxes': 20
        },
        {
            'reference': 'product_1',
            'name': 'Product 1',
            'price_without_taxes': 10.0,
            'taxes': 20.0
        },
        {
            'reference': 'product_1',
            'name': 'Product 1',
            'taxes': 20.0
        },
        {
            'reference': 'product_1',
            'name': 'Product 1',
            'price_without_taxes': 10.0,
        }
    ],
)
def test_create_product_command_validation_fields_error(fields):
    with pytest.raises(cattrs.errors.ClassValidationError):
        CreateProductCommand.from_config(fields)


def test_edit_product_command():
    command = EditProductCommand.from_config(
        {
            'identifier': '1',
            'reference': 'product_1',
            'name': 'Product 1',
            'description': 'Description of product 1',
            'price_without_taxes': 10,
            'taxes': 20
        }
    )
    result = command.data()

    assert result == {
        'identifier': 1,
        'entity': ProductDomain.from_config(
            {
                'reference': 'product_1',
                'name': 'Product 1',
                'description': 'Description of product 1',
                'price_without_taxes': 10,
                'taxes': 20
            }
        )
    }


@pytest.mark.parametrize(
    'fields',
    [
        {
            'name': 'Product 1',
            'reference': 'product_1',
            'description': 'Description of product 1',
            'price_without_taxes': 10,
            'taxes': 20
        },
        {
            'identifier': '1',
            'reference': 'product_1',
            'description': 'Description of product 1',
            'price_without_taxes': 10,
            'taxes': 20
        },
        {
            'identifier': '1',
            'name': 'Product 1',
            'description': 'Description of product 1',
            'price_without_taxes': 10,
            'taxes': 20
        },
        {
            'identifier': '1',
            'name': 'Product 1',
            'reference': 'product_1',
            'price_without_taxes': 10,
            'taxes': 20
        },
        {
            'identifier': '1',
            'name': 'Product 1',
            'reference': 'product_1',
            'price_without_taxes': 10,
        }
    ],
)
def test_create_product_command_validation_fields_error(fields):
    with pytest.raises(cattrs.errors.ClassValidationError):
        EditProductCommand.from_config(fields)
