from ..core.component import Component
from ..canvas import Canvas
from ..graph import Graph
from .default_adapter import (DefaultAdapter,
                              create_simple_adapter)


class DictAdapter(DefaultAdapter):

    def serialize(self, handler):
        dict_obj = self.adaptee
        return {key: handler.serialize(value)
                for key, value in dict_obj.iteritems()}


GraphAdapter = create_simple_adapter(['canvas'])
CanvasAdapter = create_simple_adapter(['plots'])


def register_serializers(manager):
    manager.register(DictAdapter, dict)
    manager.register(DefaultAdapter, Component)
    manager.register(GraphAdapter, Graph)
    manager.register(CanvasAdapter, Canvas)
