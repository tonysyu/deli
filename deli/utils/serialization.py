
class Serializable(object):
    """Thin wrapper around an object to provide a serialization interface"""

    def __init__(self, label, value):
        self.label = label
        self.value = value

    def serialize(self):
        return {self.label: self.value}


def iter_attrs(obj, attr_names):
    """Yield attributes appropriate for serialization.

    All `deli.core.Component` subclasses implement a `serialize` method, which
    is required for serialization. Attributes that don't implement
    a `serialize` method are wrapped in a `Serializable` object, with the
    label set to the attribute name.
    """
    for name in attr_names:
        attribute = getattr(obj, name)
        if not hasattr(attribute, 'serialize'):
            attribute = Serializable(name, attribute)
        yield attribute
