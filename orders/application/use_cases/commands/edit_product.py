from __future__ import annotations

from copy import deepcopy
from typing import Any

import cattr

from orders.application.use_cases.commands.base import ICommand
from attrs import define, asdict
from orders.domain.entities.product import ProductDomain


@define(auto_attribs=True, frozen=True)
class EditProductCommand(ICommand):
    """
    Command to edit a product

    Attributes
    ----------
    identifier : int
        The identifier of the product
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
    identifier: int
    reference: str
    name: str
    description: str
    price_without_taxes: float
    taxes: float

    def data(self) -> dict[str, Any]:
        return {
            'identifier': self.identifier,
            'entity': ProductDomain.from_config(
                asdict(
                    self,
                    filter=lambda field, value: field != 'identifier'
                )
            )
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> EditProductCommand:
        converter = deepcopy(cattr.global_converter)
        return converter.structure(config, cls)

