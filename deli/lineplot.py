""" Defines the LinePlot class.
"""
import numpy as np

from enable.api import black_color_trait, LineStyle
from traits.api import Enum, Float, List, Property, Tuple, cached_property

from .base_xy_plot import BaseXYPlot
from matplotlib.transforms import Bbox, BboxTransform


class LinePlot(BaseXYPlot):
    """ A plot consisting of a line.
    """
    # The color of the line.
    color = black_color_trait

    # The RGBA tuple for rendering lines.  It is always a tuple of length 4.
    # It has the same RGB values as color_, and its alpha value is the alpha
    # value of self.color multiplied by self.alpha.
    effective_color = Property(Tuple, depends_on=['color', 'alpha'])

    # The thickness of the line.
    line_width = Float(1.0)

    # The line dash style.
    line_style = LineStyle

    render_style = Enum("connectedpoints", "hold", "connectedhold")

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    _cached_data_pts = List

    _cached_screen_pts = List

    def get_screen_points(self):
        x = self.x_src.get_data()
        y = self.y_src.get_data()

        x0, x1 = self.x_mapper.range.low, self.x_mapper.range.high
        y0, y1 = self.y_mapper.range.low, self.y_mapper.range.high
        data_bbox = Bbox.from_extents(x0, y0, x1, y1)
        data_to_screen = BboxTransform(data_bbox, self.screen_bbox)

        xy_points = np.column_stack((x, y))
        return [data_to_screen.transform(xy_points)]

    #------------------------------------------------------------------------
    # Private methods; implements the BaseXYPlot stub methods
    #------------------------------------------------------------------------

    def _render(self, gc, points, selected_points=None):
        with gc:
            gc.set_antialias(True)
            gc.clip_to_rect(self.x, self.y, self.width, self.height)

            # Render using the normal style
            gc.set_stroke_color(self.effective_color)
            gc.set_line_width(self.line_width)
            gc.set_line_dash(self.line_style_)
            self._render_normal(gc, points)

    @classmethod
    def _render_normal(cls, gc, points):
        for line in points:
            if len(line) > 0:
                gc.begin_path()
                gc.lines(line)
                gc.stroke_path()

    def _color_changed(self):
        self.invalidate_draw()
        self.request_redraw()

    @cached_property
    def _get_effective_color(self):
        alpha = self.color_[-1] if len(self.color_) == 4 else 1
        c = self.color_[:3] + (alpha * self.alpha,)
        return c
