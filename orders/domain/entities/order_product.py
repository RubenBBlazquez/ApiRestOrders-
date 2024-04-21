from __future__ import annotations

from copy import deepcopy
from typing import Any

from attrs import define, asdict
from orders.domain.entities.base import IDomainEntity
import cattr


@define(auto_attribs=True, frozen=True)
class OrderProductDomain(IDomainEntity):
    """
    Domain entity that represents a product

    Attributes
    ----------
    reference : str
        The id of the product
    order_id : str
        The id of the order
    quantity : int
        The quantity of the product
    """
    reference: str
    order_id: int
    quantity: int

    def parameters(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> OrderProductDomain:
        converter = deepcopy(cattr.global_converter)
        return converter.structure(config, cls)