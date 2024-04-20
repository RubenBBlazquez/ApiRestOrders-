from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from attrs import define


class ICommand(ABC):
    """
    Interface that represents a command.
    """

    @abstractmethod
    def data(self) -> dict[str, Any]:
        """
        A method to return the command's data properties.
        """
        raise NotImplementedError()

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> ICommand:
        """
        A method to create a command from a configuration dictionary

        Returns
        -------
        dict
            the parameters of the command
        """
        raise NotImplementedError()


class DummyCommand(ICommand):
    """
    A dummy command to be used as a default command.
    """

    def data(self) -> dict[str, Any]:
        return {}

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> DummyCommand:
        return cls()


@define(auto_attribs=True, frozen=True)
class GetByIdCommand(ICommand):
    """
    Interface that represents a get by id command.

    Attributes
    ----------
    identifier : int
        The identifier of the entity
    """
    identifier: int

    def data(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> GetByIdCommand:
        try:
            return cls(
                identifier=config['identifier']
            )
        except KeyError:
            raise KeyError("The GetByIdCommand config must have the key 'identifier'.")
