from abc import abstractmethod

from traits.api import ABCHasStrictTraits, Adapter, Constant, List, Str
from traits.adaptation.api import AdaptationManager

from deli.core.component import Component
from deli.artist.base_artist import BaseArtist


def get_protocol(obj):
    return obj.__class__.__name__


def serialize_children(obj, children, handler):
    return {name: handler.serialize(getattr(obj, name)) for name in children}


def serialize_dict(obj, handler):
    return {key: handler.serialize(value) for key, value in obj.iteritems()}


class ISerializeFactory(ABCHasStrictTraits):

    @abstractmethod
    def serialize(self, handler):
        """ Return serialized output of object. """


class DefaultSerializationAdapter(Adapter):

    version = Constant(1)
    children = List(Str)

    def serialize(self, handler):
        obj = self.adaptee
        blob = self._serialize_required_attrs(obj)
        blob.update(serialize_children(obj, self.children, handler))
        blob.update(self._serialize_hook(handler))
        return blob

    def _serialize_required_attrs(self, obj):
        return {'__protocol__': get_protocol(obj),
                '__version__': self.version}

    def _serialize_hook(self, handler):
        return {}


class SerializationManager(AdaptationManager):

    def __init__(self, *args, **traits):
        super(SerializationManager, self).__init__(*args, **traits)

    def register(self, serialize_func, from_protocol):
        self.register_factory(serialize_func, from_protocol, ISerializeFactory)

    def serialize(self, obj):
        serialization_factory = self.adapt(obj, ISerializeFactory)
        return serialization_factory.serialize(self)


default_serialization_manager = SerializationManager()
default_serialization_manager.register(DefaultSerializationAdapter, Component)
default_serialization_manager.register(DefaultSerializationAdapter, BaseArtist)


def create_simple_serialization_adapter(children_names):
    class SimpleSerializationAdapter(DefaultSerializationAdapter):
        children = List(Str, value=children_names)
    return SimpleSerializationAdapter


from deli.graph import Graph
graph_adapter = create_simple_serialization_adapter(['canvas'])
default_serialization_manager.register(graph_adapter, Graph)


def serialize_canvas(obj):
    return {'plots': serialize_dict(obj.plots)}


class CanvasSerializationAdapter(DefaultSerializationAdapter):

    def _serialize_hook(self, handler):
        obj = self.adaptee
        return {'plots': serialize_dict(obj.plots, handler)}


from deli.canvas import Canvas
default_serialization_manager.register(CanvasSerializationAdapter, Canvas)


def serialize_list(objects):
    serialize = default_serialization_manager.serialize
    return [serialize(obj) for obj in objects]


def serialize(obj):
    """ Return serialized mapping of the given object. """
    return default_serialization_manager.serialize(obj)
