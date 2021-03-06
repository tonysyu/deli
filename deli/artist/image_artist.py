from traits.api import Array, Instance

from ..stylus.image_stylus import ImageStylus
from .base_artist import BaseArtist


class ImageArtist(BaseArtist):
    """ An artist for image data. """

    data = Array

    image = Instance(ImageStylus, ())

    def draw(self, gc, view_rect=None):
        height, width = self.data.shape[:2]
        rect_corners = self.data_to_screen.transform([(0, 0), (width, height)])
        x0, y0, x1, y1 = rect_corners.flat
        rect = x0, y0, (x1 - x0), (y1 - y0)
        with self._clipped_context(gc):
            self.image.draw(gc, self.data, rect)

    def _get_data_extents(self):
        height, width = self.data.shape[:2]
        return (0, 0, width, height)
