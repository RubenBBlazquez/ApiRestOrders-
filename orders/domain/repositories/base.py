from abc import ABC, abstractmethod
from typing import Any

from django.db.models import QuerySet

from orders.domain.entities.base import IDomainEntity

from django.db import models


class IRepository(ABC):
    """
    Interface that represents a base repository

    """

    @abstractmethod
    def get_by_id(self, identifier: int) -> models.Model:
        """
        Get an entity by its identifier

        Parameters
        ----------
        identifier : int
            The identifier of the entity

        Returns
        -------
        models.Model
            django orm model object
        """
        raise NotImplementedError()

    @abstractmethod
    def get_by_field(self, field: str, value: Any) -> QuerySet[models.Model]:
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
        QuerySet[models.Model]
            QuerySet of django orm model objects
        """
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> QuerySet[models.Model]:
        """
        Get all entities

        Returns
        -------
        QuerySet[models.Model]
            QuerySet of django orm model objects
        """
        raise NotImplementedError()

    @abstractmethod
    def save(self, entity: IDomainEntity) -> models.Model:
        """
        Save an entity

        Parameters
        ----------
        entity : IDomainEntity
            The entity to be saved

        Returns
        -------
        models.Model
            The saved entity
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, identifier: int, entity: IDomainEntity) -> models.Model:
        """
        Update an entity

        Parameters
        ----------
        identifier : int
            The identifier of the entity
        entity : IDomainEntity
            The entity to be deleted
        """
        raise NotImplementedError()
