"""
Defines the DataRange1D class.
"""
from numpy import inf

from traits.api import CFloat, Property, Trait

from .abstract_data_range import AbstractDataRange


class DataRange1D(AbstractDataRange):
    """ Represents a 1-D data range.
    """

    low = Property
    high = Property

    low_setting = Property(Trait('auto', 'auto', 'track', CFloat))
    high_setting = Property(Trait('auto', 'auto', 'track', CFloat))

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    # The "_setting" attributes correspond to what the user has "set"; the
    # "_value" attributes are the actual numerical values for the given
    # setting.

    # The user-specified low setting.
    _low_setting = Trait('auto', 'auto', 'track', CFloat)
    # The actual numerical value for the low setting.
    _low_value = CFloat(-inf)
    # The user-specified high setting.
    _high_setting = Trait('auto', 'auto', 'track', CFloat)
    # The actual numerical value for the high setting.
    _high_value = CFloat(inf)

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def refresh(self):
        self._refresh_bounds()

    #------------------------------------------------------------------------
    # Private methods (getters and setters)
    #------------------------------------------------------------------------

    def _get_low(self):
        return float(self._low_value)

    def _get_high(self):
        return float(self._high_value)

    def _refresh_bounds(self):
        bounds_list = [source.get_bounds() for source in self.sources \
                          if source.get_size() > 0]

        mins, maxes = zip(*bounds_list)

        low_start, high_start = calc_bounds(mins, maxes)

        if (self._low_value != low_start) or (self._high_value != high_start):
            self._low_value = low_start
            self._high_value = high_start
            self.updated = (self._low_value, self._high_value)

    #------------------------------------------------------------------------
    # Event handlers
    #------------------------------------------------------------------------

    def _sources_items_changed(self, event):
        self.refresh()


def calc_bounds(mins, maxes):
    """ Calculates bounds for a given 1-D set of data.

    Returns
    -------
    (min, max) for the new bounds. If either of the calculated bounds is NaN,
    returns (0,0).

    """
    real_min = min(mins)
    real_max = max(maxes)
    return real_min, real_max
