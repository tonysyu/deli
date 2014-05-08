import numpy as np

from traits.api import DelegatesTo, Instance, Property, Tuple, cached_property

from ..artist.line_artist import LineArtist
from .base_point_renderer import BasePointRenderer


class LineRenderer(BasePointRenderer):
    """ A renderer for a line plot.
    """
    # The color of the line.
    color = DelegatesTo('line')

    line = Instance(LineArtist, ())

    # The RGBA tuple for rendering lines.  It is always a tuple of length 4.
    # It has the same RGB values as color_, and its alpha value is the alpha
    # value of self.color multiplied by self.alpha.
    _effective_color = Property(Tuple, depends_on=['color', 'alpha'])

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    def get_screen_points(self):
        x = self.x_src.get_data()
        y = self.y_src.get_data()
        xy_points = np.column_stack((x, y))

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
        self.invalidate_draw()
        self.request_redraw()

    @cached_property
    def _get__effective_color(self):
        alpha = self.color_[-1] if len(self.color_) == 4 else 1
        c = self.color_[:3] + (alpha * self.alpha,)
        return c
