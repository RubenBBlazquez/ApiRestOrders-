from __future__ import annotations

from copy import deepcopy
from typing import Any

import cattr
from attr import define, asdict

from orders.domain.entities.base import IDomainEntity


@define(auto_attribs=True)
class OrderProductElement:
    """
    entity that represents a product in an order

    Attributes
    ----------
    reference : str
        The reference of the product
    quantity : int
        The quantity of the product
    product_price_without_taxes : float
        The price of the product without taxes
    product_taxes : float
        The taxes of the product
    """
    reference: str
    quantity: int
    product_price_without_taxes: float = 0
    product_taxes: float = 0

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> OrderProductElement:
        converter = deepcopy(cattr.global_converter)
        return converter.structure(config, cls)


@define(auto_attribs=True)
class OrderDomain(IDomainEntity):
    """
    Domain entity that represents an order

    Attributes
    ----------
    products : list[OrderProductElement]
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
        """
        Add a product to the order

        Parameters
        ----------
        new_order_product: OrderProductElement
            The new product to add
        """
        self.products.append(new_order_product)

    def _set_products_to_edit(
            self,
            new_products: list[OrderProductElement],
            index: int, product_to_check,
            products_to_edit: list[OrderProductElement]
    ):
        """
        update the quantity of the products that are in the new products list, but with a different quantity

        Parameters
        ----------
        new_products: list[OrderProductElement]
            The new products to compare with
        index: int
            The index of the product we are checking
        product_to_check
            The product to check

        """
        for new_product in new_products:
            equal_reference = product_to_check.reference == new_product.reference
            distinct_quantity = product_to_check.quantity != new_product.quantity

            if equal_reference and distinct_quantity:
                self.products[index].quantity = new_product.quantity
                products_to_edit.append(self.products[index])

    def _set_products_to_remove(
            self,
            product_to_check: OrderProductElement,
            index: int,
            new_products_references: list[str],
            products_to_remove: list[OrderProductElement]
    ):
        """
        It will remove the products that are not in the new products list and add them to the list of products
        to update the OrderProduct entities in database later

        Parameters
        ----------
        product_to_check: OrderProductElement
            The product to check
        index: int
            The index of the product to remove
        new_products_references: list[str]
            The references of the new products
        products_to_remove: list[OrderProductElement]
            The products to remove

        """
        if product_to_check.reference not in new_products_references:
            products_to_remove.append(self.products[index])
            del self.products[index]

    def _get_products_to_check_existence(self, new_products: list[OrderProductElement]):
        """
        This method returns the products that are not in the order but are in the new products list,
        so, we have to check if they exist first before adding them to the list of products

        Parameters
        ----------
        new_products: list[OrderProductElement]
            The new products to compare with

        """
        products_to_check = []
        actual_products_references = [product.reference for product in self.products]

        for new_product in new_products:
            if new_product.reference not in actual_products_references:
                products_to_check.append(new_product)

        return products_to_check

    def sync_order_with_new_products(
            self,
            new_products: list[OrderProductElement]
    ) -> tuple[list[OrderProductElement], list[OrderProductElement]]:
        """
        Method to synchronize the order with new products.
        It will remove the products that are not in the new products list
        and update the quantity of the products that are in the new products list, but with a different quantity.
        Finally, it will return the products that are not in the order
        because we have to check if exists first before adding them to the list of products.

        Parameters
        ----------
        new_products: list[OrderProductElement]
            The new products to compare with

        Returns
        -------
        tuple[list[OrderProductElement], list[OrderProductElement], list[OrderProductElement]]
            The products we have to check if exists first, the products to remove, and the products to edit
        """
        new_products_references = [product.reference for product in new_products]
        new_products_to_check_existence = self._get_products_to_check_existence(
            new_products
        )
        products_to_remove = []
        products_to_edit = []

        for index, product in enumerate(self.products.copy()):
            self._set_products_to_edit(new_products, index, product, products_to_edit)
            self._set_products_to_remove(product, index, new_products_references, products_to_remove)

        return new_products_to_check_existence, products_to_remove, products_to_edit

    def update_total_price_without_taxes(self) -> None:
        """
        Update the total price of the order without taxes

        """
        self.total_price_without_taxes = sum(
            product.quantity * product.product_price_without_taxes
            for product in self.products
        )

    def update_total_price_with_taxes(self) -> None:
        """
        Update the total price of the order with taxes

        """
        self.total_price_with_taxes = sum(
            product.quantity * (product.product_price_without_taxes + product.product_taxes)
            for product in self.products
        )

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> OrderDomain:
        converter = deepcopy(cattr.global_converter)
        return converter.structure(config)
