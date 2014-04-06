"""
Defines the LinearMapper class, which maps from a 1-D region in data space
into a 1-D output space.
"""
from traits.api import Float

from .base_1d_mapper import Base1DMapper


class LinearMapper(Base1DMapper):
    """ Maps a 1-D data space to and from screen space by specifying a range in
    data space and a corresponding fixed line in screen space.
    """

    # Number of screen space units per data space unit.
    _scale = Float(1.0)

    def map_screen(self, data_array):
        """ map_screen(data_array) -> screen_array

        Overrides AbstractMapper. Maps values from data space into screen space.
        """
        self._compute_scale()
        return (data_array - self.range.low) * self._scale + self.low_pos

    def _compute_scale(self):
        r = self.range
        screen_range = self.high_pos - self.low_pos
        data_range = r.high - r.low

        self._scale = screen_range / data_range
