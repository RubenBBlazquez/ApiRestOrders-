from abc import ABC, abstractmethod

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
    def get_all(self) -> list[models.Model]:
        """
        Get all entities

        Returns
        -------
        list[models.Model]
            List of django orm model objects
        """
        raise NotImplementedError()

    @abstractmethod
    def save(self, entity) -> models.Model:
        """
        Save an entity

        Parameters
        ----------
        entity : object
            The entity to save

        Returns
        -------
        models.Model
            The saved entity
        """
        raise NotImplementedError()
