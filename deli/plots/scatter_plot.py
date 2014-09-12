from traits.api import DelegatesTo, Instance

from ..stylus.marker_stylus import MarkerStylus
from .base_point_plot import BasePointPlot


class ScatterPlot(BasePointPlot):
    """ A plot for a data points that should display as markers
    """
    # The color of the markers.
    color = DelegatesTo('marker')

    marker = Instance(MarkerStylus, ())

    #--------------------------------------------------------------------------
    #  Private interface
    #--------------------------------------------------------------------------

    def _render(self, gc, points, selected_points=None):
        with gc:
            gc.clip_to_rect(*self.screen_bbox.bounds)
            self.marker.draw(gc, points)
