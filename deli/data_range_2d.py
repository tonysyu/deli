"""
Defines the DataRange2D class.
"""
import numpy as np
from matplotlib.transforms import Bbox

from traits.api import HasStrictTraits, Instance


class DataRange2D(HasStrictTraits):
    """ A range for 2D data. """

    #: Bounding box for data sources.
    bbox = Instance(Bbox)

    def _bbox_default(self):
        return Bbox.from_extents(np.inf, np.inf, -np.inf, -np.inf)

    def update_x_data(self, x):
        x_span = calc_bounds(x, self.bbox.intervalx)
        if x_span is not None:
            self.bbox.intervalx = x_span

    def update_y_data(self, y):
        y_span = calc_bounds(y, self.bbox.intervaly)
        if y_span is not None:
            self.bbox.intervaly = y_span


def calc_bounds(x, current_bounds):
    x_min, x_max = current_bounds
    x_lo = min(np.min(x), x_min)
    x_hi = max(np.max(x), x_max)
    if x_lo < x_min or x_hi > x_max:
        return (x_lo, x_hi)
    else:
        return None
