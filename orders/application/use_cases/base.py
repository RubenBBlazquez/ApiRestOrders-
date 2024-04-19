from abc import abstractmethod, ABC

from django.db import models

from orders.domain.repositories.base import IRepository


class IUseCase(ABC):
    """
    Interface that represents an use case
    """

    @abstractmethod
    def execute(self, **kwargs):
        """
        Execute the use case

        Parameters
        ----------
        kwargs
            The keyword arguments
        """
        raise NotImplementedError()


class ListUseCase(IUseCase):
    """
    Interface that represents a list use case

    Attributes
    ----------
    repository : IRepository
        The repository from we will get the entities
    """

    def __init__(self, repository: IRepository):
        self.repository = repository

    def execute(self, **kwargs) -> list[models.Model]:
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

    def execute(self, **kwargs) -> models.Model:
        """
        Execute the use case to get an entity by its identifier

        Parameters
        ----------
        kwargs
         identifier: int
            The identifier of the entity to retrieve.

        Returns
        -------
        models.Model
            The retrieved entity.

        Raises
        ------
        ValueError
            If 'identifier' is missing from kwargs or is not an integer.
        """
        identifier = kwargs.get('identifier')

        if identifier is None or not isinstance(identifier, int):
            raise ValueError("An integer 'identifier' must be provided")

        return self.repository.get_by_id(identifier=identifier)