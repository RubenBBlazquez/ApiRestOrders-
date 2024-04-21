from __future__ import annotations

from copy import deepcopy
from typing import Any

import cattr
from attr import define, asdict

from orders.domain.entities.base import IDomainEntity


@define(auto_attribs=True, frozen=True)
class OrderProductElement:
    """
    entity that represents a product in an order

    Attributes
    ----------
    reference : str
        The reference of the product
    quantity : int
        The quantity of the product
    price_without_taxes : float
        The price of the product without taxes
    taxes : float
        The taxes of the product
    """
    reference: str
    quantity: int
    price_without_taxes: float = 0
    taxes: float = 0

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> OrderProductElement:
        converter = deepcopy(cattr.global_converter)
        return converter.structure(config)


@define(auto_attribs=True)
class OrderDomain(IDomainEntity):
    """
    Domain entity that represents an order

    Attributes
    ----------
    products : list[OrderProductDomain]
        The products of the order
    total_price_without_taxes : float
        The total price of the order without taxes
    total_price_with_taxes : float
        The total price of the order with taxes
    """
    products: list[OrderProductElement]
    total_price_without_taxes: float = 0
    total_price_with_taxes: float = 0

    def parameters(self) -> dict[str, Any]:
        return asdict(self)

    def add_product(self, new_order_product: OrderProductElement) -> None:
        self.products.append(new_order_product)

    def remove_product(self, product_to_remove: OrderProductElement) -> None:
        for product in self.products:
            if product.reference == product_to_remove.reference:
                self.products.remove(product)

    def edit_product(self, new_product: OrderProductElement) -> None:
        for index, product in enumerate(self.products):
            if product.reference == new_product.reference:
                self.products[index] = new_product

    def update_total_price_without_taxes(self) -> None:
        self.total_price_without_taxes = sum(
            product.quantity * product.price_without_taxes
            for product in self.products
        )

    def update_total_price_with_taxes(self) -> None:
        self.total_price_with_taxes = sum(
            product.quantity * (product.price_without_taxes + product.taxes)
            for product in self.products
        )

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> OrderDomain:
        converter = deepcopy(cattr.global_converter)
        return converter.structure(config)
