from django.db import models

from orders.domain.repositories.base import IRepository
from orders.infrastructure.models import Product


class ProductRepository(IRepository):
    """
    Class that represents the Order repository
    """

    def get_by_id(self, identifier: int) -> models.Model:
        return Product.objects.filter(pk=identifier).first()

    def get_all(self) -> list[models.Model]:
        return Product.objects.all()

    def save(self, entity) -> models.Model:
        pass
