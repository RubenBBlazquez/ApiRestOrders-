from django.db import models

from orders.domain.repositories.base import IRepository
from orders.infrastructure.models.order import Order


class OrderRepository(IRepository):
    """
    Class that represents the Order repository
    """

    def get_by_id(self, identifier: int) -> models.Model:
        return Order.objects.filter(pk=identifier).first()

    def get_all(self) -> list[models.Model]:
        return Order.objects.all()

    def save(self, entity) -> models.Model:
        pass

    def update(self, identifier: int, entity) -> models.Model:
        pass
