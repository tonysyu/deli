from atom.api import Instance
from enaml.core.declarative import Declarative

from ..artist.base_artist import BaseArtist as _BaseArtist


class BaseArtist(Declarative):

    deli_artist = Instance(_BaseArtist)
