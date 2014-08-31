import numpy as np

from enable.api import ColorTrait, LineStyle
from traits.api import CFloat, HasStrictTraits, Range

from ..style import config


class LineArtist(HasStrictTraits):
    """ A Flyweight object for drawing lines.
    """

    # The color of the grid lines.
    color = ColorTrait(config.get('line.color'))

    # The style (i.e., dash pattern) of the grid lines.
    style = LineStyle(config.get('line.style'))

    # The thickness, in pixels, of the grid lines.
    width = CFloat(config.get('line.width'))

    # Overall alpha value of the image. Ranges from 0.0 for transparent to 1.0
    alpha = Range(0.0, 1.0, 1.0)

    def update_style(self, gc):
        gc.set_alpha(self.alpha)
        gc.set_line_width(self.width)
        gc.set_line_dash(self.style_)
        gc.set_stroke_color(self.color_)

    def draw(self, gc, points):
        """ Draw a series of straight line segments between points.

        Parameters
        ----------
        gc : GraphicsContext
            The graphics context where elements are drawn.
        points : array, shape (N, 2)
            Draw a line through a series of (x, y) points.
        """
        with gc:
            self.update_style(gc)
            gc.begin_path()
            gc.lines(points)
            gc.stroke_path()

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

        with gc:
            self.update_style(gc)
            gc.begin_path()
            gc.line_set(starts, ends)
            gc.stroke_path()
