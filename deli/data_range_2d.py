"""
Defines the DataRange2D class.
"""
from numpy import inf
from matplotlib.transforms import Bbox

from traits.api import (Any, CFloat, Instance, on_trait_change, Property,
                        Trait, Tuple)

from .abstract_data_range import AbstractDataRange
from .data_range_1d import DataRange1D


class DataRange2D(AbstractDataRange):
    """ A range for 2D data. """

    low = Property  # (2,) array of lower-left x,y
    high = Property  # (2,) array of upper-right x,y

    low_setting = Property
    high_setting = Property

    # Property for the range in the x-dimension.
    x_range = Property

    # Property for the range in the y-dimension.
    y_range = Property

    #: Bounding box for data sources.
    bbox = Instance(Bbox)

    def _bbox_default(self):
        x0, x1 = self._xrange.low, self._xrange.high
        y0, y1 = self._yrange.low, self._yrange.high
        return Bbox.from_extents(x0, y0, x1, y1)

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

    def _get_x_range(self):
        return self._xrange

    def _get_y_range(self):
        return self._yrange

    @on_trait_change('_xrange:updated')
    def _x_range_updated(self):
        self.bbox.intervalx = (self._xrange.low, self._xrange.high)

    @on_trait_change('_yrange:updated')
    def _y_range_updated(self):
        self.bbox.intervaly = (self._yrange.low, self._yrange.high)
