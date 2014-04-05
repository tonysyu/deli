"""
Defines the DataRange1D class.
"""
from numpy import inf, ndarray

from traits.api import Bool, Callable, CFloat, Float, Property, Trait

from .base_data_range import BaseDataRange


class DataRange1D(BaseDataRange):
    """ Represents a 1-D data range.
    """

    low = Property
    high = Property

    low_setting = Property(Trait('auto', 'auto', 'track', CFloat))
    high_setting = Property(Trait('auto', 'auto', 'track', CFloat))

    tight_bounds = Bool(True)

    bounds_func = Callable

    margin = Float(0.05)

    epsilon = CFloat(1.0e-10)

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
    # AbstractRange interface
    #------------------------------------------------------------------------

    def mask_data(self, data):
        """ Returns a mask array, indicating whether values in the given array
        are inside the range.

        Implements AbstractDataRange.
        """
        return ((data.view(ndarray) >= self._low_value) &
                (data.view(ndarray) <= self._high_value))

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

        low_start, high_start = \
                 calc_bounds(self._low_setting, self._high_setting,
                             mins, maxes, self.epsilon,
                             self.tight_bounds, margin=self.margin,
                             bounds_func=self.bounds_func)

        if (self._low_value != low_start) or (self._high_value != high_start):
            self._low_value = low_start
            self._high_value = high_start
            self.updated = (self._low_value, self._high_value)

    #------------------------------------------------------------------------
    # Event handlers
    #------------------------------------------------------------------------

    def _sources_items_changed(self, event):
        self.refresh()


def calc_bounds(low_set, high_set, mins, maxes, epsilon, tight_bounds,
                margin=0.08, track_amount=0, bounds_func=None):
    """ Calculates bounds for a given 1-D set of data.

    Returns
    -------
    (min, max) for the new bounds. If either of the calculated bounds is NaN,
    returns (0,0).

    """
    real_min = min(mins)
    real_max = max(maxes)
    return real_min, real_max
