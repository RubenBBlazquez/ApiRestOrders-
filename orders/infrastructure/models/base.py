from abc import abstractmethod

from orders.domain.entities.base import IDomainEntity


class ICustomModel:
    """
    Interface that will be implemented by all models in the infrastructure layer
    and define a method to convert the model to a domain entity.
    """

    @abstractmethod
    def to_domain(self) -> IDomainEntity:
        """
        Convert the model to a domain entity

        Returns
        -------
        IDomainEntity
            Domain entity
        """
        raise NotImplementedError
