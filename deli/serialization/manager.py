from abc import abstractmethod

from traits.api import ABCHasStrictTraits
from traits.adaptation.api import AdaptationManager


class ISerializeFactory(ABCHasStrictTraits):

    @abstractmethod
    def serialize(self, handler):
        """ Return serialized output of object. """


class SerializationManager(AdaptationManager):

    def __init__(self, *args, **traits):
        super(SerializationManager, self).__init__(*args, **traits)

    def register(self, serialize_func, from_protocol):
        self.register_factory(serialize_func, from_protocol, ISerializeFactory)

    def serialize(self, obj):
        serialization_factory = self.adapt(obj, ISerializeFactory)
        return serialization_factory.serialize(self)
