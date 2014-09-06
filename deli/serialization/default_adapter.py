from traits.api import Adapter, Constant, List, Str


def get_protocol(obj):
    return obj.__class__.__name__


def serialize_children(obj, children, handler):
    return {name: handler.serialize(getattr(obj, name)) for name in children}


class DefaultAdapter(Adapter):

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


def create_simple_adapter(children_names):
    class SimpleAdapter(DefaultAdapter):
        children = List(Str, value=children_names)
    return SimpleAdapter
