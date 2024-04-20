from django.db import models

from orders.domain.repositories.base import IRepository
from orders.domain.entities.product import ProductDomain
from orders.infrastructure.models import Product


class ProductRepository(IRepository):
    """
    Class that represents the Order repository
    """

    def get_by_id(self, identifier: int) -> Product:
        return Product.objects.filter(pk=identifier).first()

    def get_all(self) -> Product:
        return Product.objects.all()

    def save(self, entity: ProductDomain) -> models.Model:
        product = Product(**entity.parameters())
        product.save()
        return product

    def update(self, identifier: int, entity: ProductDomain) -> models.Model:
        product = Product.objects.get(pk=identifier)

        product.reference = entity.reference
        product.name = entity.name
        product.description = entity.description
        product.price_without_taxes = entity.price_without_taxes
        product.taxes = entity.taxes
        product.save()

        return product
