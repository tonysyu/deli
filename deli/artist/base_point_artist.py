""" Defines the base class for XY artists.
"""
import numpy as np

from traits.api import CArray, Range

from .base_artist import BaseArtist


class BasePointArtist(BaseArtist):
    """ Base class for simple point data artists that consist of a single x data
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

    #--------------------------------------------------------------------------
    #  BaseArtist interface
    #--------------------------------------------------------------------------

    def get_screen_points(self):
        xy_points = np.column_stack((self.x_data, self.y_data))
        return self.data_to_screen.transform(xy_points)

    def _get_data_extents(self):
        x = self.x_data
        y = self.y_data
        return (x.min(), y.min(), x.max(), y.max())
