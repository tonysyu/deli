import numpy as np

from .line_stylus import LineStylus


class SegmentStylus(LineStylus):
    """ A Flyweight object for drawing line segemnts.

    Line segments, unlike lines drawn by `LineStylus`, are strictly straight
    line pairs of start and end points ((x0, y0), (x1, y2)).
    """

    def draw(self, gc, starts, ends):
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
