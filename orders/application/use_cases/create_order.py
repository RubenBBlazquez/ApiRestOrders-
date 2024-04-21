from orders.application.use_cases.base import CreateUseCase
from orders.application.use_cases.commands.create_order import CreateOrderCommand
from orders.domain.entities.order import OrderDomain, OrderProductElement
from orders.domain.entities.order_product import OrderProductDomain
from orders.infrastructure.repositories.order_product_repository import OrderProductRepository
from orders.infrastructure.repositories.order_repository import OrderRepository
from orders.infrastructure.repositories.product_repository import ProductRepository


class CreateOrderUseCase(CreateUseCase):
    """
    Class that represents the creation of an order

    Attributes
    ----------
    product_repository : ProductRepository
        The product repository
    """

    def __init__(
            self,
            order_repository: OrderRepository,
            product_repository: ProductRepository,
            order_product_repository: OrderProductRepository
    ):
        super().__init__(order_repository)
        self.product_repository = product_repository
        self.order_product_repository = order_product_repository

    def execute(self, command: CreateOrderCommand):
        products = command.products
        not_valid_products = []
        order_domain = OrderDomain(
            products=[],
            total_price_without_taxes=0,
            total_price_with_taxes=0
        )

        for order_product in products:
            product_query_set = self.product_repository.get_by_field(
                field='reference', value=order_product.reference
            )

            if not product_query_set.exists():
                not_valid_products.append(order_product.reference)
                continue

            product = product_query_set.first()
            order_product_element_domain = OrderProductElement(
                reference=product.reference,
                quantity=order_product.quantity,
                product_price_without_taxes=float(product.price_without_taxes),
                product_taxes=float(product.taxes)
            )
            order_domain.add_product(order_product_element_domain)

        order_domain.update_total_price_without_taxes()
        order_domain.update_total_price_with_taxes()
        order_entity = self.repository.save(order_domain)

        for order_product in order_domain.products:
            self.order_product_repository.save(
                OrderProductDomain(
                    reference=order_product.reference,
                    quantity=order_product.quantity,
                    order_id=order_entity.id,
                )
            )

        return not_valid_products, order_entity
