import numpy as np

from traits.api import DelegatesTo, Instance

from ..artist.line_artist import LineArtist
from .base_point_plot import BasePointPlot


class LinePlot(BasePointPlot):
    """ A plot for line data.
    """
    # The color of the line.
    color = DelegatesTo('line')

    line = Instance(LineArtist, ())

    #------------------------------------------------------------------------
    #  Public interface
    #------------------------------------------------------------------------

    def get_screen_points(self):
        xy_points = np.column_stack((self.x_data, self.y_data))
        return [self.data_to_screen.transform(xy_points)]

    #--------------------------------------------------------------------------
    #  Private interface
    #--------------------------------------------------------------------------

    def _render(self, gc, line_segments, selected_points=None):
        with gc:
            gc.clip_to_rect(*self.screen_bbox.bounds)
            self.line.update_style(gc)
            for points in line_segments:
                self.line.draw(gc, points)

    def _color_changed(self):
        self.request_redraw()
