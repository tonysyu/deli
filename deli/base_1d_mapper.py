""" Defines the Base1DMapper class.
"""
from traits.api import Instance, Float, Property

from .abstract_mapper import AbstractMapper
from .data_range_1d import DataRange1D
from .utils import switch_trait_handler


class Base1DMapper(AbstractMapper):
    """ Defines an abstract mapping from a 1-D region in input space to a 1-D
    region in output space.
    """

    # The data-space bounds of the mapper.
    range = Instance(DataRange1D)

    # The screen space position of the lower bound of the data space.
    low_pos = Float(0.0)

    # The screen space position of the upper bound of the data space.
    high_pos  = Float(1.0)

    # Convenience property to get low and high positions in one structure.
    # Must be a tuple (low_pos, high_pos).
    screen_bounds = Property

    #------------------------------------------------------------------------
    # Event handlers
    #------------------------------------------------------------------------

    def _low_pos_changed(self):
        self.updated = True

    def _high_pos_changed(self):
        self.updated = True

    def _range_changed(self, old, new):
        switch_trait_handler(old, new, 'updated', self._range_change_handler)
        self.updated = new

    def _range_change_handler(self, obj, name, new):
        pass

    def _set_screen_bounds(self, new_bounds):
        self.set(low_pos = new_bounds[0], trait_change_notify=False)
        self.set(high_pos = new_bounds[1], trait_change_notify=False)
        self.updated = True
