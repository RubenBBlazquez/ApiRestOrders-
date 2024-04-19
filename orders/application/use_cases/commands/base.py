from abc import ABC, abstractmethod
from typing import Any


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


class DummyCommand(ICommand):
    """
    A dummy command to be used as a default command.
    """

    def data(self) -> dict[str, Any]:
        return {}


class GetByIdCommand(ICommand):
    """
    Interface that represents a get by id command.

    Attributes
    ----------
    id : int
        The identifier of the entity
    """

    def __init__(self, identifier: int):
        self.identifier = identifier

    def data(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier
        }
