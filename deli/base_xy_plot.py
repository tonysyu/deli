""" Defines the base class for XY plots.
"""
from matplotlib.transforms import Bbox, BboxTransform

from traits.api import Disallow, Instance, Property, Range

from .abstract_plot_renderer import AbstractPlotRenderer
from .abstract_data_source import AbstractDataSource
from .array_data_source import ArrayDataSource


class BaseXYPlot(AbstractPlotRenderer):
    """ Base class for simple X-vs-Y plots that consist of a single x
    data array and a single y data array.

    Subclasses handle the actual rendering, but this base class takes care of
    most of making sure events are wired up between mappers and data or screen
    space changes, etc.
    """

    _ = Disallow

    #------------------------------------------------------------------------
    # Data-related traits
    #------------------------------------------------------------------------

    # The data source to use for the x coordinate.
    x_src = Instance(ArrayDataSource)

    # The data source to use as y points.
    y_src = Instance(AbstractDataSource)

    #: Bounding box for data in plot.
    data_bbox = Instance(Bbox)

    #: Transform from data space to screen space.
    data_to_screen = Instance(BboxTransform)

    def _data_to_screen_default(self):
        return BboxTransform(self.data_bbox, self.screen_bbox._bbox)

    #------------------------------------------------------------------------
    # Appearance-related traits
    #------------------------------------------------------------------------

    # Overall alpha value of the image. Ranges from 0.0 for transparent to 1.0
    alpha = Range(0.0, 1.0, 1.0)

    #------------------------------------------------------------------------
    # Convenience readonly properties for common annotations
    #------------------------------------------------------------------------

    # Read-only property for x-axis.
    x_axis = Property
    # Read-only property for y-axis.
    y_axis = Property
    # Read-only property for labels.
    labels = Property

    #------------------------------------------------------------------------
    # Other public traits
    #------------------------------------------------------------------------

    # Overrides the default background color trait in PlotComponent.
    bgcolor = "transparent"

    #------------------------------------------------------------------------
    # Concrete methods below
    #------------------------------------------------------------------------

    #------------------------------------------------------------------------
    # PlotComponent interface
    #------------------------------------------------------------------------

    def _draw_plot(self, gc, view_bounds=None, mode="normal"):
        """ Draws the 'plot' layer.
        """
        self._draw_component(gc, view_bounds, mode)

    def _draw_component(self, gc, view_bounds=None, mode="normal"):
        # This method should be folded into self._draw_plot(), but is here for
        # backwards compatibilty with non-draw-order stuff.

        pts = self.get_screen_points()
        self._render(gc, pts)
