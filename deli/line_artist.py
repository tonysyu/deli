import numpy as np

from enable.api import ColorTrait, LineStyle
from traits.api import HasStrictTraits, CFloat


class LineArtist(HasStrictTraits):
    """ A Flyweight object for drawing lines.
    """

    # The color of the grid lines.
    color = ColorTrait('black')

    # The style (i.e., dash pattern) of the grid lines.
    style = LineStyle('solid')

    # The thickness, in pixels, of the grid lines.
    width = CFloat(1)

    def update_context(self, gc):
        # XXX: Rename to update_style since "context" is overloaded.
        gc.set_line_width(self.width)
        gc.set_line_dash(self.style_)
        gc.set_stroke_color(self.color_)

    def draw_segments(self, gc, starts, ends):
        """ Draw a series of straight line segments between points.

        Parameters
        ----------
        gc : GraphicsContext
            The graphics context where elements are drawn.
        starts, ends : array, shape (N, 2) or (2,)
            Starting and ending points for straight line segments. Each row
            of `starts` and `ends` define an (x, y) point.
        """
        # Turn arrays with shape (2,) to (1, 2)
        starts = np.atleast_2d(starts)
        ends = np.atleast_2d(ends)

        gc.begin_path()
        gc.line_set(starts, ends)
        gc.stroke_path()
