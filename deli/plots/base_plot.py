""" Defines the base class for XY plots.
"""
from traits.api import Instance, Property, Tuple

from ..core.component import Component
from ..layout.bounding_box import BoundingBox
from ..layout.bbox_transform import BboxTransform


class BasePlot(Component):
    """ Base class for all plots.

    Unlike artists, plots may contain the data that they render. Plots are
    simply specific types of plots: For example, line-plots, marker-plots, and
    bar-plots, may all be the same data associated with different plots.  As
    a result, plots may use a few different artists to compose a plot; for
    example, a box-and-whisker plot might have separate artists to draw
    rectangles, error-bars (whiskers), and points (outliers).
    """

    #------------------------------------------------------------------------
    # Data-related traits
    #------------------------------------------------------------------------

    #: The extents of the data (x_min, y_min, x_max, y_max)
    data_extents = Property(Tuple)

    #: Bounding box for data in the plot graph. Note that this bounding box
    #: does not just describe the data in this plot; it's the currently
    #: displayed limits of the plot in data space.
    data_bbox = Instance(BoundingBox)

    #: Transform from data space to screen space.
    data_to_screen = Instance(BboxTransform)

    #: Transform from data space to screen space.
    screen_to_data = Property(Instance(BboxTransform),
                              depends_on='data_to_screen')

    def _data_to_screen_default(self):
        return BboxTransform(self.data_bbox, self.screen_bbox)

    def _get_screen_to_data(self):
        return self.data_to_screen.inverted()

    #--------------------------------------------------------------------------
    #  BasePlot interface
    #--------------------------------------------------------------------------

    def _get_data_extents(self):
        msg = "`BasePlot` subclasses must implement `_get_data_extents`"
        raise NotImplementedError(msg)
