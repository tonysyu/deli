from ..core.component import Component
from ..canvas import Canvas
from ..graph import Graph
from .default_adapter import (DefaultSerializationAdapter,
                              create_simple_serialization_adapter)
from . import utils


GraphSerializationAdapter = create_simple_serialization_adapter(['canvas'])


class CanvasSerializationAdapter(DefaultSerializationAdapter):

    def _serialize_hook(self, handler):
        canvas = self.adaptee
        return {'plots': utils.serialize_dict(canvas.plots, handler)}


def register_serializers(manager):
    manager.register(DefaultSerializationAdapter, Component)
    manager.register(GraphSerializationAdapter, Graph)
    manager.register(CanvasSerializationAdapter, Canvas)
