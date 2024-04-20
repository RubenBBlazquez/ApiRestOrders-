from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
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

    @method_decorator(require_POST)
    def post(self, request: WSGIRequest):
        body = request.POST.dict()
        create_use_case = CreateUseCase(self.repository)
        command = CreateProductCommand.from_config(body)
        entity = create_use_case.execute(command)

        return JsonResponse(
            self.serializer.from_model(entity).data,
            status=200,
            safe=False
        )

    @method_decorator(require_http_methods(["PUT"]))
    def put(self, request: WSGIRequest):
        data = safe_loads(request.body.decode('utf-8'))
        edit_use_case = EditUseCase(self.repository)
        command = EditProductCommand.from_config(data)
        entity = edit_use_case.execute(command)

        return JsonResponse(
            self.serializer.from_model(entity).data,
            status=200,
            safe=False
        )
