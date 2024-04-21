from __future__ import annotations
from copy import deepcopy
from typing import Any

import cattr
from attr import define, asdict

from orders.application.use_cases.commands.base import ICommand
from orders.domain.entities.order import OrderDomain, OrderProductElement


@define(auto_attribs=True, frozen=True)
class CreateOrderCommand(ICommand):
    """
    Command to create a product

    Attributes
    ----------
    products : list[OrderProductDomain]
        The products of the order
    """

    products: list[OrderProductElement]

    def data(self) -> dict[str, Any]:
        return {
            'products': [asdict(product) for product in self.products],
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> CreateOrderCommand:
        converter = deepcopy(cattr.global_converter)
        return converter.structure(config, cls)

