from typing import Any
from django.db.models import QuerySet

from orders.domain.entities.order import OrderDomain
from orders.domain.repositories.base import IRepository
from orders.infrastructure.models.order import Order, OrderProduct


class OrderRepository(IRepository):
    """
    Class that represents the Order repository
    """

    def get_by_id(self, identifier: int) -> Order:
        return Order.objects.filter(pk=identifier).first()

    def get_by_field(self, field: str, value: Any) -> QuerySet[Order]:
        return Order.objects.filter(**{field: value})

    def get_all(self) -> QuerySet[Order]:
        return Order.objects.all()

    def save(self, entity: OrderDomain) -> Order:
        order = Order(
            total_price_without_taxes=entity.total_price_without_taxes,
            total_price_with_taxes=entity.total_price_with_taxes
        )

        order.save()
        return order

    def update(self, identifier: int, entity: OrderDomain) -> Order:
        pass
