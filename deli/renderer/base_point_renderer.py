""" Defines the base class for XY plots.
"""
from traits.api import Instance, Range

from ..abstract_data_source import AbstractDataSource
from ..array_data_source import ArrayDataSource
from .base_renderer import BaseRenderer


class BasePointRenderer(BaseRenderer):
    """ Base class for simple point data plots that consist of a single x data
    array and a single y data array.

    Subclasses handle the actual rendering, but this base class takes care of
    most of making sure events are wired up between mappers and data or screen
    space changes, etc.
    """

    #------------------------------------------------------------------------
    # Data-related traits
    #------------------------------------------------------------------------

    # The data source to use for the x coordinate.
    x_src = Instance(ArrayDataSource)

    # The data source to use as y points.
    y_src = Instance(AbstractDataSource)

    #------------------------------------------------------------------------
    # Appearance-related traits
    #------------------------------------------------------------------------

    # Overall alpha value of the image. Ranges from 0.0 for transparent to 1.0
    alpha = Range(0.0, 1.0, 1.0)

    #------------------------------------------------------------------------
    # PlotComponent interface
    #------------------------------------------------------------------------

    def _draw_plot(self, gc, view_bounds=None, mode="normal"):
        """ Draws the 'plot' layer.
        """
        pts = self.get_screen_points()
        self._render(gc, pts)
