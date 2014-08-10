""" Defines the base class for XY plots.
"""
from traits.api import CArray, Range

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

    #: The data for the x coordinate.
    x_data = CArray

    #: The data for the y coordinate.
    y_data = CArray

    #------------------------------------------------------------------------
    # Appearance-related traits
    #------------------------------------------------------------------------

    #: Overall alpha value of the image. Ranges from 0.0 for transparent to 1.0
    alpha = Range(0.0, 1.0, 1.0)

    #------------------------------------------------------------------------
    # Component interface
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
        x = self.x_data
        y = self.y_data
        return (x.min(), y.min(), x.max(), y.max())
