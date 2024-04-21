import cattrs
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from orders.application.use_cases.base import CreateUseCase, EditUseCase
from orders.application.use_cases.commands.create_product import CreateProductCommand
from orders.application.use_cases.commands.edit_product import EditProductCommand
from orders.infrastructure.endpoints.apis.base import BaseAPI
from orders.utils import safe_loads


class ProductAPI(BaseAPI):
    """
    Class that represents the Product API
    """

    @csrf_exempt
    @method_decorator(require_POST)
    def post(self, request: WSGIRequest):
        data = safe_loads(request.body.decode('utf-8'))
        create_use_case = CreateUseCase(self.repository)

        try:
            command = CreateProductCommand.from_config(data)
        except cattrs.errors.ClassValidationError as e:
            return JsonResponse(
                {
                    "error": "Invalid structure in the request body",
                    "valid_structure": {
                        "reference": "str - The product reference",
                        "name": "str - The product name",
                        "description": "str - The product description",
                        "price_without_taxes": "float - The product price without taxes",
                        "taxes": "float - The product taxes"
                    },
                },
                status=400,
                safe=False
            )

        entity = create_use_case.execute(command)

        return JsonResponse(
            {
                "created_product": self.serializer.from_model(entity).data
            },
            status=200,
            safe=False
        )

    @csrf_exempt
    @method_decorator(require_http_methods(["PUT"]))
    def put(self, request: WSGIRequest):
        data = safe_loads(request.body.decode('utf-8'))
        edit_use_case = EditUseCase(self.repository)
        try:
            command = EditProductCommand.from_config(data)
        except cattrs.errors.ClassValidationError as e:
            return JsonResponse(
                {
                    "error": "Invalid structure in the request body",
                    "valid_structure": {
                        "identifier": "int - The product identifier",
                        "reference": "str - The product reference",
                        "name": "str - The product name",
                        "description": "str - The product description",
                        "price_without_taxes": "float - The product price without taxes",
                        "taxes": "float - The product taxes"
                    },
                },
                status=400,
                safe=False
            )

        entity = edit_use_case.execute(command)

        return JsonResponse(
            {
                "edited_product": self.serializer.from_model(entity).data
            },
            status=200,
            safe=False
        )
