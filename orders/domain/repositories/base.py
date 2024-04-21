from abc import ABC, abstractmethod
from typing import Any
from django.db.models import QuerySet
from orders.domain.entities.base import IDomainEntity
from orders.infrastructure.models.base import ICustomModel


class IRepository(ABC):
    """
    Interface that represents a base repository

    """

    @abstractmethod
    def get_by_id(self, identifier: int) -> ICustomModel:
        """
        Get an entity by its identifier

        Parameters
        ----------
        identifier : int
            The identifier of the entity

        Returns
        -------
        ICustomModel
            django orm model object that inherits from ICustomModel
        """
        raise NotImplementedError()

    @abstractmethod
    def get_by_field(self, field: str, value: Any) -> QuerySet[ICustomModel]:
        """
        Get an entity by a field

        Parameters
        ----------
        field : str
            The field of the entity
        value : Any
            The value of the field

        Returns
        -------
        QuerySet[ICustomModel]
            QuerySet of django orm model object that inherits from ICustomModel
        """
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> QuerySet[ICustomModel]:
        """
        Get all entities

        Returns
        -------
        QuerySet[ICustomModel]
            QuerySet of django orm model object that inherits from ICustomModel

        """
        raise NotImplementedError()

    @abstractmethod
    def save(self, entity: IDomainEntity) -> ICustomModel:
        """
        Save an entity

        Parameters
        ----------
        entity : IDomainEntity
            The entity to be saved

        Returns
        -------
        ICustomModel
            django orm model object that inherits from ICustomModel

        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, identifier: int, entity: IDomainEntity) -> ICustomModel:
        """
        Update an entity

        Parameters
        ----------
        identifier : int
            The identifier of the entity
        entity : IDomainEntity
            The entity to be deleted

        Returns
        -------
        ICustomModel
            django orm model object that inherits from ICustomModel

        """
        raise NotImplementedError()

    def delete(self, entity: IDomainEntity) -> ICustomModel:
        """
        Update an entity

        Parameters
        ----------
        entity : IDomainEntity
            The entity to be deleted

        Returns
        -------
        ICustomModel
            django orm model object that inherits from ICustomModel

        """
        raise NotImplementedError()
