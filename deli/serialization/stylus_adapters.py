from deli.stylus.base_stylus import BaseStylus
from .default_adapter import DefaultAdapter


def register_serializers(manager):
    manager.register(DefaultAdapter, BaseStylus)
