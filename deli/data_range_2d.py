"""
Defines the DataRange2D class.
"""
import numpy as np

from traits.api import HasStrictTraits, Instance

from .layout.bounding_box import BoundingBox


class DataRange2D(HasStrictTraits):
    """ A range for 2D data. """

    #: Bounding box for data sources.
    bbox = Instance(BoundingBox)

    def _bbox_default(self):
        return BoundingBox.from_extents(np.inf, np.inf, -np.inf, -np.inf)
