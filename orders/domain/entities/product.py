from __future__ import annotations

from copy import deepcopy
from typing import Any

from attrs import define, asdict
from orders.domain.entities.base import IDomainEntity
import cattr


@define(auto_attribs=True, frozen=True)
class ProductDomain(IDomainEntity):
    """
    Domain entity that represents a product

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

    def parameters(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> ProductDomain:
        converter = deepcopy(cattr.global_converter)
        return converter.structure(config, cls)