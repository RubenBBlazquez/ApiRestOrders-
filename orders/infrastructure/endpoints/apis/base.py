from abc import ABC
from typing import Type

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from orders.application.use_cases.base import GetByIdUseCase, GetAllUseCase, CreateUseCase
from orders.application.use_cases.commands.base import GetByIdCommand, DummyCommand
from orders.domain.repositories.base import IRepository
from orders.infrastructure.serializers.base import CustomSerializer


class IApi(ABC):

    @method_decorator(require_GET)
    def get(self, request: WSGIRequest):
        pass

    @method_decorator(require_POST)
    def post(self, request: WSGIRequest):
        pass

    @method_decorator(require_http_methods(["PUT"]))
    def put(self, request: WSGIRequest):
        pass


class BaseAPI(IApi):
    def __init__(self, repository: IRepository, serializer: Type[CustomSerializer]):
        self.repository = repository
        self.serializer = serializer

    @method_decorator(require_GET)
    def get(self, request: WSGIRequest):
        identifier = request.GET.get('id')

        if identifier:
            use_case = GetByIdUseCase(self.repository)
            command = GetByIdCommand(identifier)
            entity = use_case.execute(command)

            return JsonResponse(
                self.serializer.from_model(entity).data,
                status=200,
                safe=False
            )

        use_case = GetAllUseCase(self.repository)
        command = DummyCommand()
        entities = use_case.execute(command)

        return JsonResponse(
            data=self.serializer.from_model(entities, True).data,
            safe=False,
            status=200
        )
