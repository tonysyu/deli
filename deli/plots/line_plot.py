from traits.api import DelegatesTo, Instance

from ..artist.line_artist import LineArtist
from .base_point_plot import BasePointPlot


class LinePlot(BasePointPlot):
    """ A plot for line data.
    """
    # The color of the line.
    color = DelegatesTo('line')

    line = Instance(LineArtist, ())

    #--------------------------------------------------------------------------
    #  Private interface
    #--------------------------------------------------------------------------

    def _render(self, gc, points, selected_points=None):
        with gc:
            gc.clip_to_rect(*self.screen_bbox.bounds)
            self.line.draw(gc, points)

    def _color_changed(self):
        self.request_redraw()

    def _get_artists(self):
        return (self.line,)
