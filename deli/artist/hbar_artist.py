import numpy as np

from traits.api import Instance

from deli.artist.base_point_artist import BasePointArtist
from deli.stylus.rect_stylus import RectangleStylus
from deli.utils.drawing import hline_to_rect_corners


def bars_from_points(x, y, data_to_screen, x0=0, height=None):
    """ Return rectangles in screen-space for x/y points in data-space. """
    if height is None:
        height = np.min(np.diff(y))

    corner0, corner1 = hline_to_rect_corners(y, x0, x, height)

    origins = data_to_screen.transform(corner0)
    sizes = data_to_screen.transform(corner1) - origins
    return np.hstack([origins, sizes])


class HBarArtist(BasePointArtist):
    """ An artist for bar plot data. """

    stylus = Instance(RectangleStylus, ())

    def draw(self, gc, view_rect=None):
        bars = self._get_bar_data()
        with self._clipped_context(gc):
            for rect in bars:
                self.stylus.draw(gc, rect)

    def _get_bar_data(self):
        x, y = self.x_data, self.y_data
        return bars_from_points(x, y, self.data_to_screen, height=0.5)
