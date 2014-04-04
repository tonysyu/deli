"""
Defines the LinearMapper class, which maps from a 1-D region in data space
into a 1-D output space.
"""
from traits.api import Bool, Float

from .base_1d_mapper import Base1DMapper


class LinearMapper(Base1DMapper):
    """ Maps a 1-D data space to and from screen space by specifying a range in
    data space and a corresponding fixed line in screen space.
    """

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    # Number of screen space units per data space unit.
    _scale = Float(1.0)
    # Is the range of the screen space empty?
    _null_screen_range = Bool(False)
    # Is the range of the data space empty?
    _null_data_range = Bool(False)

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def map_screen(self, data_array):
        """ map_screen(data_array) -> screen_array

        Overrides AbstractMapper. Maps values from data space into screen space.
        """
        self._compute_scale()
        return (data_array - self.range.low) * self._scale + self.low_pos

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _compute_scale(self):
        if self._cache_valid:
            return

        r = self.range
        screen_range = self.high_pos - self.low_pos
        data_range = r.high - r.low

        self._null_screen_range = False

        self._scale = screen_range / data_range
        self._null_data_range = bool(self._scale == 0.0)

        self._cache_valid = True
