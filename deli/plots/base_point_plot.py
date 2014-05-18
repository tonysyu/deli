""" Defines the base class for XY plots.
"""
from traits.api import CArray, Instance, Property, Range

from ..abstract_data_source import AbstractDataSource
from ..array_data_source import ArrayDataSource
from .base_plot import BasePlot


class BasePointPlot(BasePlot):
    """ Base class for simple point data plots that consist of a single x data
    array and a single y data array.

    Subclasses handle the actual plotting, but this base class takes care of
    most of making sure events are wired up between mappers and data or screen
    space changes, etc.
    """

    #------------------------------------------------------------------------
    # Data-related traits
    #------------------------------------------------------------------------

    #: The data source to use for the x coordinate.
    x_src = Instance(ArrayDataSource)

    #: The data source to use as y points.
    y_src = Instance(AbstractDataSource)

    #: Convenience property for creating `x_src`.
    x_data = Property(CArray)

    #: Convenience property for creating `y_src`.
    y_data = Property(CArray)

    #------------------------------------------------------------------------
    # Appearance-related traits
    #------------------------------------------------------------------------

    #: Overall alpha value of the image. Ranges from 0.0 for transparent to 1.0
    alpha = Range(0.0, 1.0, 1.0)

    #------------------------------------------------------------------------
    # PlotComponent interface
    #------------------------------------------------------------------------

    def _draw_plot(self, gc, view_bounds=None):
        """ Draws the 'plot' layer.
        """
        pts = self.get_screen_points()
        self._render(gc, pts)

    #--------------------------------------------------------------------------
    #  BasePlot interface
    #--------------------------------------------------------------------------

    def _get_data_extents(self):
        x = self.x_src.get_data()
        y = self.y_src.get_data()
        return (x.min(), y.min(), x.max(), y.max())

    #--------------------------------------------------------------------------
    #  Traits definitions
    #--------------------------------------------------------------------------

    def _set_x_data(self, x):
        self.x_src = ArrayDataSource(x)

    def _set_y_data(self, y):
        self.y_src = ArrayDataSource(y)
