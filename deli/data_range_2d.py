"""
Defines the DataRange2D class.
"""
from numpy import inf

from traits.api import Any, CFloat, Instance, Property, Trait, Tuple

from .abstract_data_range import AbstractDataRange
from .data_range_1d import DataRange1D


class DataRange2D(AbstractDataRange):
    """ A range on (2-D) image data.
    """

    low = Property  # (2,) array of lower-left x,y
    high = Property  # (2,) array of upper-right x,y

    low_setting = Property
    high_setting = Property

    # Property for the range in the x-dimension.
    x_range = Property

    # Property for the range in the y-dimension.
    y_range = Property

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    # The user-specified low settings.
    _low_setting = Trait(('auto', 'auto'), Any)
    # The actual numerical values for the low setting.
    _low_value = Trait((-inf, -inf), Tuple(CFloat, CFloat))
    # The user-specified high settings.
    _high_setting = Trait(('auto', 'auto'), Any)
    # The actual numerical value for the high setting.
    _high_value = Trait((inf, inf), Tuple(CFloat, CFloat))

    # DataRange1D for the x-dimension.
    _xrange = Instance(DataRange1D, args=())
    # DataRange1D for the y-dimension.
    _yrange = Instance(DataRange1D, args=())

    def __init__(self, *args, **kwargs):
        super(DataRange2D, self).__init__(*args, **kwargs)

    def _get_x_range(self):
        return self._xrange

    def _get_y_range(self):
        return self._yrange
