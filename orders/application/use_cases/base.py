from abc import abstractmethod, ABC

from django.db import models

from orders.application.use_cases.commands.base import ICommand
from orders.domain.repositories.base import IRepository


class IUseCase(ABC):
    """
    Interface that represents an use case
    """

    @abstractmethod
    def execute(self, command: ICommand):
        """
        Execute the use case

        Parameters
        ----------
        command : ICommand
            The command where the use case will get the data from
        """
        raise NotImplementedError()


class GetAllUseCase(IUseCase):
    """
    Interface that represents a list use case

    Attributes
    ----------
    repository : IRepository
        The repository from we will get the entities
    """

    def __init__(self, repository: IRepository):
        self.repository = repository

    def execute(self, command: ICommand) -> list[models.Model]:
        return self.repository.get_all()


class GetByIdUseCase(IUseCase):
    """
    Interface that represents a get use case

    Attributes
    ----------
    repository : IRepository
        The repository from we will get the entity
    """

    def __init__(self, repository: IRepository):
        self.repository = repository

    def execute(self, command: ICommand) -> models.Model:
        """
        Execute the use case to get an entity by its identifier

        Parameters
        ----------
        command : ICommand
            The command where the use case will get the data from

        Returns
        -------
        models.Model
            The retrieved entity.

        Raises
        ------
        ValueError
            If 'identifier' is missing from kwargs or is not an integer.
        """
        return self.repository.get_by_id(**command.data())
