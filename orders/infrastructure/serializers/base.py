from __future__ import annotations
from abc import abstractmethod, ABC

from django.db import models
from rest_framework import serializers


class CustomSerializer:
    @classmethod
    @abstractmethod
    def from_model(cls, model_object: models.Model) -> serializers.ModelSerializer:
        raise NotImplementedError()
