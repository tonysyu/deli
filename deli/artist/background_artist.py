from traits.api import Instance, Property

from ..layout.bounding_box import BoundingBox
from ..stylus.rect_stylus import RectangleStylus
from .base_artist import BaseArtist


class BackgroundArtist(BaseArtist):

    screen_bbox = Instance(BoundingBox)

    fill_color = Property

    stylus = Instance(RectangleStylus)

    def _set_fill_color(self, color):
        self.stylus.fill_color = color

    def _stylus_default(self):
        return RectangleStylus(edge_color='none')

    def draw(self, gc, view_rect=None):
        self.stylus.draw(gc, self.screen_bbox.rect)
