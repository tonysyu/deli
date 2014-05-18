from traits.api import Array, Instance

from ..artist.image_artist import ImageArtist
from .base_plot import BasePlot


class ImagePlot(BasePlot):
    """ A plot for image data. """

    data = Array

    image = Instance(ImageArtist, ())

    def _draw_plot(self, gc, view_bounds=None):
        height, width = self.data.shape[:2]
        rect_corners = self.data_to_screen.transform([(0, 0), (width, height)])
        x0, y0, x1, y1 = rect_corners.flat
        rect = x0, y0, (x1 - x0), (y1 - y0)
        with gc:
            gc.clip_to_rect(*self.screen_bbox.bounds)
            self.image.draw(gc, self.data, rect)

    def _get_data_extents(self):
        height, width = self.data.shape[:2]
        return (0, 0, width, height)
