from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class IDomainEntity(ABC):
    """
    Interface that represents a domain entity
    """

    @classmethod
    @abstractmethod
    def from_config(cls, config: dict[str, Any]) -> IDomainEntity:
        """
        A method to create a domain entity from a configuration dictionary

        Returns
        -------
        dict
            the parameters of the entity
        """
        raise NotImplementedError()
