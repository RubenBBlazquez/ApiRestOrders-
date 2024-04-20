from __future__ import annotations

from copy import deepcopy
from typing import Any

from attrs import define, asdict
from orders.domain.entities.base import IDomainEntity
import cattr


@define(auto_attribs=True, frozen=True)
class ProductDomain(IDomainEntity):
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