from collections import Mapping

from traits.adaptation.api import AdaptationManager

from deli.core.component import Component
from deli.artist.base_artist import BaseArtist


def get_protocol(obj):
    return obj.__class__.__name__


def serialize_default(obj):
    return {'__protocol__': get_protocol(obj), '__version__': 1}


class SerializationManager(AdaptationManager):

    def __init__(self, *args, **traits):
        super(SerializationManager, self).__init__(*args, **traits)

    def register(self, serialize_func, from_protocol):
        self.register_factory(serialize_func, from_protocol, Mapping)

    def serialize(self, obj):
        return self.adapt(obj, Mapping)


default_serialization_manager = SerializationManager()
default_serialization_manager.register(serialize_default, Component)
default_serialization_manager.register(serialize_default, BaseArtist)


def serialize_dict(obj):
    serialize = default_serialization_manager.serialize
    return {key: serialize(value) for key, value in obj.iteritems()}


default_serialization_manager.register(serialize_dict, dict)


def serialize_with_default_attrs(func):
    def wrapped(obj, *args, **kwargs):
        blob = serialize_default(obj)
        blob.update(func(obj, *args, **kwargs))
        return blob
    return wrapped


@serialize_with_default_attrs
def serialize_graph(obj):
    return serialize_children(obj, ['canvas'])


from deli.graph import Graph
default_serialization_manager.register(serialize_graph, Graph)


@serialize_with_default_attrs
def serialize_canvas(obj):
    return {'plots': serialize_dict(obj.plots)}


from deli.canvas import Canvas
default_serialization_manager.register(serialize_canvas, Canvas)


def serialize_children(obj, children_names):
    serialize = default_serialization_manager.serialize
    print [serialize(getattr(obj, name)) for name in children_names]
    return {name: serialize(getattr(obj, name))
            for name in children_names}


def serialize_list(objects):
    serialize = default_serialization_manager.serialize
    return [serialize(obj) for obj in objects]


def serialize(obj):
    """ Return serialized mapping of the given object. """
    return default_serialization_manager.serialize(obj)
