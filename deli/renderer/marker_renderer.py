import numpy as np

from traits.api import DelegatesTo, Instance

from ..artist.marker_artist import MarkerArtist
from .base_point_renderer import BasePointRenderer


class MarkerRenderer(BasePointRenderer):
    """ A renderer for a marker (scatter) plot.
    """
    # The color of the markers.
    color = DelegatesTo('marker')

    marker = Instance(MarkerArtist, ())

    #------------------------------------------------------------------------
    #  Public interface
    #------------------------------------------------------------------------

    def get_screen_points(self):
        x = self.x_src.get_data()
        y = self.y_src.get_data()
        xy_points = np.column_stack((x, y))

        return self.data_to_screen.transform(xy_points)

    #--------------------------------------------------------------------------
    #  Private interface
    #--------------------------------------------------------------------------

    def _render(self, gc, points, selected_points=None):
        with gc:
            gc.clip_to_rect(*self.screen_bbox.bounds)
            self.marker.update_style(gc)
            self.marker.draw(gc, points)
