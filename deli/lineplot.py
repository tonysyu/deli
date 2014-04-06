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
        return [self.map_screen(ary) for ary in self._cached_data_pts]

    #------------------------------------------------------------------------
    # Private methods; implements the BaseXYPlot stub methods
    #------------------------------------------------------------------------

    def _gather_points(self):
        """
        Collects the data points that are within the bounds of the plot and
        caches them.
        """
        index = self.index.get_data()
        value = self.value.get_data()

        # Check to see if the data is completely outside the view region
        for ds, rng in ((self.index, self.index_range), (self.value, self.value_range)):
            low, high = ds.get_bounds()

        index_max = len(value)
        index = index[:index_max]

        # Split the index and value raw data into non-NaN chunks
        nan_mask = np.invert(np.isnan(value)) & np.invert(np.isnan(index))
        blocks = [b for b in arg_find_runs(nan_mask, "flat") if nan_mask[b[0]] != 0]

        points = []
        for block in blocks:
            start, end = block
            block_index = index[start:end]
            block_value = value[start:end]
            index_mask = self.index_mapper.range.mask_data(block_index)

            runs = [r for r in arg_find_runs(index_mask, "flat") \
                    if index_mask[r[0]] != 0]
            # Expand the width of every group of points so we draw the lines
            # up to their next point, outside the plot area
            for run in runs:
                start, end = run

                run_data = ( block_index[start:end],
                             block_value[start:end] )
                run_data = np.column_stack(run_data)

                points.append(run_data)

        self._cached_data_pts = points

    def _render(self, gc, points, selected_points=None):
        with gc:
            gc.set_antialias(True)
            gc.clip_to_rect(self.x, self.y, self.width, self.height)

            render_method_dict = {
                    "connectedpoints": self._render_normal
                    }
            render = render_method_dict.get(self.render_style, self._render_normal)

            # Render using the normal style
            gc.set_stroke_color(self.effective_color)
            gc.set_line_width(self.line_width)
            gc.set_line_dash(self.line_style_)
            render(gc, points)

    @classmethod
    def _render_normal(cls, gc, points):
        for ary in points:
            if len(ary) > 0:
                gc.begin_path()
                gc.lines(ary)
                gc.stroke_path()

    def _color_changed(self):
        self.invalidate_draw()
        self.request_redraw()

    @cached_property
    def _get_effective_color(self):
        alpha = self.color_[-1] if len(self.color_) == 4 else 1
        c = self.color_[:3] + (alpha * self.alpha,)
        return c
