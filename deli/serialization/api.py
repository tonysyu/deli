from importlib import import_module
from .manager import SerializationManager


def register_default_serializers(manager):
    for mod_name in ('.core_adapters', '.artist_adapters'):
        module = import_module(mod_name, package='deli.serialization')
        module.register_serializers(manager)

serialization_manager = SerializationManager()
register_default_serializers(serialization_manager)


def serialize(obj):
    """ Return serialized mapping of the given object. """
    return serialization_manager.serialize(obj)
