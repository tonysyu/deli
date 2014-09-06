import numpy as np

from ..core.component import Component
from ..canvas import Canvas
from ..graph import Graph
from .default_adapter import (DefaultAdapter, create_simple_adapter)


class ValueAdapter(DefaultAdapter):

    def serialize(self, handler):
        return self.adaptee


class ListAdapter(DefaultAdapter):

    def serialize(self, handler):
        return [handler.serialize(value) for value in self.adaptee]


class DictAdapter(DefaultAdapter):

    def serialize(self, handler):
        dict_obj = self.adaptee
        return {key: handler.serialize(value)
                for key, value in dict_obj.iteritems()}


def register_serializers(manager):
    manager.register(ValueAdapter, int)
    manager.register(ValueAdapter, float)
    manager.register(ValueAdapter, str)
    manager.register(ListAdapter, list)
    manager.register(DictAdapter, dict)
    manager.register(ValueAdapter, np.ndarray)
