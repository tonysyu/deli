from traits.api import DelegatesTo, Instance

from ..artist.marker_artist import MarkerArtist
from .base_point_plot import BasePointPlot


class ScatterPlot(BasePointPlot):
    """ A plot for a data points that should display as markers
    """
    # The color of the markers.
    color = DelegatesTo('marker')

    marker = Instance(MarkerArtist, ())

    #--------------------------------------------------------------------------
    #  Private interface
    #--------------------------------------------------------------------------

    def _render(self, gc, points, selected_points=None):
        with gc:
            gc.clip_to_rect(*self.screen_bbox.bounds)
            self.marker.update_style(gc)
            self.marker.draw(gc, points)
