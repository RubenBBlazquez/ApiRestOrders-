from django.db import models

from orders.domain.entities.base import IDomainEntity
from orders.infrastructure.models.base import ICustomModel
from orders.domain.entities.product import ProductDomain


class Product(ICustomModel, models.Model):
    """
    Model that represents a product.
    """
    id = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_without_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_domain(self) -> IDomainEntity:
        return ProductDomain(
            reference=self.reference,
            name=self.name,
            description=self.description,
            price_without_taxes=float(self.price_without_taxes),
            taxes=float(self.taxes)
        )
