import numpy as np
from atom.api import Typed
from enaml.core.declarative import d_

from ..artist.line_artist import LineArtist as _LineArtist
from .base_artist import BaseArtist


class LineArtist(BaseArtist):

    x_data = d_(Typed(np.ndarray))
    y_data = d_(Typed(np.ndarray))

    def _default_deli_artist(self):
        return _LineArtist(x_data=self.x_data, y_data=self.y_data)
