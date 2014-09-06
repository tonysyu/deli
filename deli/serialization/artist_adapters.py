from deli.artist.base_artist import BaseArtist
from .default_adapter import DefaultSerializationAdapter


def register_serializers(manager):
    manager.register(DefaultSerializationAdapter, BaseArtist)
