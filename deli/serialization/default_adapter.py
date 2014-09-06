from traits.api import Adapter, Constant, List, Str

from .utils import get_protocol, serialize_children


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


def create_simple_serialization_adapter(children_names):
    class SimpleSerializationAdapter(DefaultSerializationAdapter):
        children = List(Str, value=children_names)
    return SimpleSerializationAdapter
