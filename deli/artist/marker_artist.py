from traits.api import DelegatesTo, Instance

from ..stylus.marker_stylus import MarkerStylus
from .base_point_artist import BasePointArtist


class MarkerArtist(BasePointArtist):
    """ An artist for data points that should display as markers. """
    # The color of the markers.
    color = DelegatesTo('marker')

    marker = Instance(MarkerStylus, ())

    def draw(self, gc, view_rect=None):
        points = self.get_screen_points()
        with self._clipped_context(gc):
            self.marker.draw(gc, points)
