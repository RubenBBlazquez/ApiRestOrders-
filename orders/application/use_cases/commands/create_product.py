from __future__ import annotations

from copy import deepcopy
from typing import Any

import cattr

from orders.application.use_cases.commands.base import ICommand
from attrs import define, asdict
from orders.domain.entities.product import ProductDomain


@define(auto_attribs=True, frozen=True)
class CreateProductCommand(ICommand):
    """
    Command to create a product

    Attributes
    ----------
    reference : str
        The reference of the product
    name : str
        The name of the product
    description : str
        The description of the product
    price_without_taxes : float
        The price of the product without taxes
    taxes : float
        The taxes of the product

    """

    reference: str
    name: str
    description: str
    price_without_taxes: float
    taxes: float

    def data(self) -> dict[str, Any]:
        return {
            'entity': ProductDomain.from_config(
                asdict(self)
            )
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> CreateProductCommand:
        converter = deepcopy(cattr.global_converter)
        return converter.structure(config, cls)

