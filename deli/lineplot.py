""" Defines the LinePlot class.
"""
import numpy as np

from enable.api import black_color_trait, LineStyle
from traits.api import Enum, Float, List, Property, Tuple, cached_property
from traitsui.api import Item, View

from .base import arg_find_runs
from .base_xy_plot import BaseXYPlot


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

    # Traits UI View for customizing the plot.
    traits_view = View(Item("color", style="custom"), "line_width", "line_style",
                       buttons=["OK", "Cancel"])

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    _cached_data_pts = List

    _cached_screen_pts = List

    def get_screen_points(self):
        self._gather_points()
        return [self.map_screen(pts) for pts in self._cached_data_pts]

    #------------------------------------------------------------------------
    # Private methods; implements the BaseXYPlot stub methods
    #------------------------------------------------------------------------

    def _gather_points(self):
        """
        Collects the data points that are within the bounds of the plot and
        caches them.
        """
        x = self.x_src.get_data()
        y = self.y_src.get_data()

        # Split the raw x/y data into non-NaN chunks
        nan_mask = np.invert(np.isnan(y)) & np.invert(np.isnan(x))
        blocks = [b for b in arg_find_runs(nan_mask, "flat") if nan_mask[b[0]] != 0]

        points = []
        for block in blocks:
            start, end = block
            x_segment = x[start:end]
            y_segment = y[start:end]
            x_mask = self.x_mapper.range.mask_data(x_segment)

            runs = [r for r in arg_find_runs(x_mask, "flat") \
                    if x_mask[r[0]] != 0]
            # Expand the width of every group of points so we draw the lines
            # up to their next point, outside the plot area
            for run in runs:
                start, end = run

                run_data = ( x_segment[start:end],
                             y_segment[start:end] )
                run_data = np.column_stack(run_data)

                points.append(run_data)

        self._cached_data_pts = points

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
