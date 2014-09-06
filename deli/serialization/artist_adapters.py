from deli.artist.base_artist import BaseArtist
from .default_adapter import DefaultAdapter


def register_serializers(manager):
    manager.register(DefaultAdapter, BaseArtist)
