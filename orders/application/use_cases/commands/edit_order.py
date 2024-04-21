from __future__ import annotations
from copy import deepcopy
from typing import Any

import cattr
from attr import define, asdict

from orders.application.use_cases.commands.base import ICommand
from orders.domain.entities.order import OrderProductElement


@define(auto_attribs=True, frozen=True)
class EditOrderCommand(ICommand):
    """
    Command to edit an order

    Attributes
    ----------
    identifier : int
        The identifier of the order
    products : list[OrderProductElement]
        The products of the order
    """
    identifier: int
    products: list[OrderProductElement]

    def data(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'products': [asdict(product) for product in self.products],
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> EditOrderCommand:
        converter = deepcopy(cattr.global_converter)
        return converter.structure(config, cls)

