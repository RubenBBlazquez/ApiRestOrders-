import cattrs.errors
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from orders.application.use_cases.commands.create_order import CreateOrderCommand
from orders.application.use_cases.commands.edit_order import EditOrderCommand
from orders.application.use_cases.create_order import CreateOrderUseCase
from orders.application.use_cases.edit_order import EditOrderUseCase
from orders.infrastructure.endpoints.apis.base import BaseAPI
from orders.infrastructure.repositories.order_product_repository import OrderProductRepository
from orders.infrastructure.repositories.order_repository import OrderRepository
from orders.infrastructure.repositories.product_repository import ProductRepository
from orders.utils import safe_loads


class OrdersAPI(BaseAPI):
    """
    Class that represents the Product API

    Attributes
    ----------
    product_repository : ProductRepository
        The product repository
    order_product_repository : OrderProductRepository
        The order product repository
    """

    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        order_product_repository: OrderProductRepository,
        serializer
    ):
        super().__init__(order_repository, serializer)
        self.product_repository = product_repository
        self.order_product_repository = order_product_repository

    @csrf_exempt
    @method_decorator(require_POST)
    def post(self, request: WSGIRequest):
        data = safe_loads(request.body.decode('utf-8'))
        create_use_case = CreateOrderUseCase(
            self.repository,
            self.product_repository,
            self.order_product_repository
        )

        try:
            command = CreateOrderCommand.from_config(data)
        except cattrs.errors.ClassValidationError as e:
            return JsonResponse(
                {
                    "error": "Invalid structure in the request body",
                    "valid_structure": {
                        'products': [
                            {'product_id': 'int', 'quantity': 'int'}
                        ]
                    },
                },
                status=400,
                safe=False
            )

        not_valid_products, entity = create_use_case.execute(command)
        order = self.serializer.from_model(entity).data

        return JsonResponse(
            {
                'created_order': order,
                'not_valid_products': not_valid_products
            },
            status=200,
            safe=False
        )

    @csrf_exempt
    @method_decorator(require_http_methods(["PUT"]))
    def put(self, request: WSGIRequest):
        data = safe_loads(request.body.decode('utf-8'))
        edit_use_case = EditOrderUseCase(
            self.repository,
            self.product_repository,
            self.order_product_repository
        )

        try:
            command = EditOrderCommand.from_config(data)
        except cattrs.errors.ClassValidationError as e:
            return JsonResponse(
                {
                    "error": "Invalid structure in the request body",
                    "valid_structure": {
                        "identifier": "int - The order identifier",
                        'products': [
                            {'product_id': 'int', 'quantity': 'int'}
                        ]
                    },
                },
                status=400,
                safe=False
            )

        not_valid_products, entity = edit_use_case.execute(command)
        order = self.serializer.from_model(entity).data

        return JsonResponse(
            {
                'edited_order': order,
                'not_valid_products': not_valid_products
            },
            status=200,
            safe=False
        )