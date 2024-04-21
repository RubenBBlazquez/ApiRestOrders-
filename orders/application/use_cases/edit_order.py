from typing import cast

from orders.application.use_cases.base import CreateUseCase
from orders.application.use_cases.commands.edit_order import EditOrderCommand
from orders.domain.entities.order import OrderDomain, OrderProductElement
from orders.domain.entities.order_product import OrderProductDomain
from orders.infrastructure.models import Order
from orders.infrastructure.repositories.order_product_repository import OrderProductRepository
from orders.infrastructure.repositories.order_repository import OrderRepository
from orders.infrastructure.repositories.product_repository import ProductRepository


class EditOrderUseCase(CreateUseCase):
    """
    Class that represents the creation of an order

    Attributes
    ----------
    product_repository : ProductRepository
        The product repository
    """

    def __init__(
            self,
            order_repository: OrderRepository,
            product_repository: ProductRepository,
            order_product_repository: OrderProductRepository
    ):
        super().__init__(order_repository)
        self.product_repository = product_repository
        self.order_product_repository = order_product_repository

    def _remove_order_products(self, orders_products_to_remove: list[OrderProductElement], order_id: int):
        for product_to_remove in orders_products_to_remove:
            self.order_product_repository.delete(
                OrderProductDomain(
                    reference=product_to_remove.reference,
                    quantity=product_to_remove.quantity,
                    order_id=order_id
                )
            )

    def _edit_order_products(self, orders_products_to_edit: list[OrderProductElement], order_id: int):
        for product_to_edit in orders_products_to_edit:
            self.order_product_repository.update(
                None,
                OrderProductDomain(
                    reference=product_to_edit.reference,
                    quantity=product_to_edit.quantity,
                    order_id=order_id
                )
            )

    def _check_and_create_order_product(
            self,
            new_products_to_check: list[OrderProductElement],
            order_id: int, order_domain: OrderDomain,
            not_valid_products: list[str]
    ):
        for order_product in new_products_to_check:
            product_query_set = self.product_repository.get_by_field(
                field='reference', value=order_product.reference
            )

            if not product_query_set.exists():
                not_valid_products.append(order_product.reference)
                continue

            product = product_query_set.first()
            order_product_element_domain = OrderProductElement(
                reference=product.reference,
                quantity=order_product.quantity,
                product_price_without_taxes=float(product.price_without_taxes),
                product_taxes=float(product.taxes)
            )
            order_domain.add_product(order_product_element_domain)
            self.order_product_repository.save(
                OrderProductDomain(
                    reference=order_product.reference,
                    quantity=order_product.quantity,
                    order_id=order_id
                )
            )

    def execute(self, command: EditOrderCommand):
        new_products = command.products
        not_valid_products = []
        order_entity = cast(Order, self.repository.get_by_id(command.identifier))
        order_domain = cast(OrderDomain, order_entity.to_domain())
        new_products_to_check, products_to_remove, products_to_edit = (
            order_domain.sync_order_with_new_products(new_products)
        )

        self._check_and_create_order_product(new_products_to_check, order_entity.id, order_domain, not_valid_products)
        self._remove_order_products(products_to_remove, order_entity.id)
        self._edit_order_products(products_to_edit, order_entity.id)

        order_domain.update_total_price_without_taxes()
        order_domain.update_total_price_with_taxes()
        order_entity = self.repository.update(order_entity.id, order_domain)

        return not_valid_products, order_entity
