from typing import Any, Optional

from django.db.models import QuerySet
from orders.domain.entities.order_product import OrderProductDomain
from orders.domain.repositories.base import IRepository
from orders.infrastructure.models import Product
from orders.infrastructure.models.order import OrderProduct, Order


class OrderProductRepository(IRepository):
    """
    Class that represents the Order repository
    """

    def get_by_id(self, identifier: int) -> OrderProduct:
        return OrderProduct.objects.filter(pk=identifier).first()

    def get_by_field(self, field: str, value: Any) -> QuerySet[OrderProduct]:
        return OrderProduct.objects.filter(**{field: value})

    def get_all(self) -> QuerySet[OrderProduct]:
        return OrderProduct.objects.all()

    def save(self, entity: OrderProductDomain) -> OrderProduct:
        order_product = OrderProduct(
            product=Product.objects.get(reference=entity.reference),
            quantity=entity.quantity,
            order=Order.objects.get(pk=entity.order_id)
        )
        order_product.save()
        return order_product

    def update(self, identifier: Optional[int], entity: OrderProductDomain) -> OrderProduct:
        order_product = OrderProduct.objects.get(product__reference=entity.reference, order__id=entity.order_id)

        order_product.product = Product.objects.get(reference=entity.reference)
        order_product.quantity = entity.quantity
        order_product.order = Order.objects.get(pk=entity.order_id)
        order_product.save()

        return order_product

    def delete(self, entity: OrderProductDomain) -> None:
        OrderProduct.objects.filter(
            product__reference=entity.reference,
            order__id=entity.order_id
        ).delete()
