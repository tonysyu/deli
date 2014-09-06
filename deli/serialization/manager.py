from abc import abstractmethod

from traits.api import ABCHasStrictTraits, Type
from traits.adaptation.api import AdaptationManager


class ISerializeFactory(ABCHasStrictTraits):

    @abstractmethod
    def serialize(self, handler):
        """ Return serialized output of object. """


class SerializationManager(AdaptationManager):

    _interface = Type(ISerializeFactory)

    def __init__(self, *args, **traits):
        super(SerializationManager, self).__init__(*args, **traits)

    def register(self, serialize_func, from_protocol):
        self.register_factory(serialize_func, from_protocol, self._interface)

    def serialize(self, obj):
        serialization_factory = self.adapt(obj, self._interface)
        return serialization_factory.serialize(self)

    def is_serializable(self, obj):
        return self.supports_protocol(obj, self._interface)

    def copy(self):
        cls = self.__class__
        # This copy isn't really necessary since traits `Dict`s are copied.
        adaptation_offers = self._adaptation_offers.copy()
        return cls(_adaptation_offers=adaptation_offers)
