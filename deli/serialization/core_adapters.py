from ..core.component import Component
from ..canvas import Canvas
from ..graph import Graph


component_attrs = ['origin', 'size']
graph_attrs = component_attrs + ['canvas']
canvas_attrs = component_attrs + ['plots']


def register_serializers(manager):
    manager.register_attrs(component_attrs, Component)
    manager.register_attrs(graph_attrs, Graph)
    manager.register_attrs(canvas_attrs, Canvas)
