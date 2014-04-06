""" Defines the ArrayDataSource class."""
import numpy as np

from traits.api import Tuple

from .base import NumericalSequenceTrait, SortOrderTrait
from .abstract_data_source import AbstractDataSource


class ArrayDataSource(AbstractDataSource):
    """ A data source representing a single, continuous array of numerical data.
    """

    # The sort order of the data.
    sort_order = SortOrderTrait

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    # The data array itself.
    _data = NumericalSequenceTrait

    # Cached values of min and max as long as **_data** doesn't change.
    _cached_bounds = Tuple

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def __init__(self, data=np.array([]), sort_order="none", **kw):
        AbstractDataSource.__init__(self, **kw)
        self.set_data(data, sort_order)

    def set_data(self, newdata, sort_order=None):
        """ Sets the data, and optionally the sort order, for this data source.

        Parameters
        ----------
        newdata : array
            The data to use.
        sort_order : SortOrderTrait
            The sort order of the data
        """
        self._data = newdata
        if sort_order is not None:
            self.sort_order = sort_order
        self._compute_bounds()
        self.data_changed = True

    #------------------------------------------------------------------------
    # AbstractDataSource interface
    #------------------------------------------------------------------------

    def get_data(self):
        """ Returns the data for this data source, or 0.0 if it has no data.

        Implements AbstractDataSource.
        """
        return self._data

    def get_size(self):
        """get_size() -> int

        Implements AbstractDataSource.
        """
        return len(self._data)

    def get_bounds(self):
        """ Returns the minimum and maximum values of the data source's data.

        Implements AbstractDataSource.
        """
        return self._cached_bounds

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _compute_bounds(self, data=None):
        """ Computes the minimum and maximum values of self._data.

        If a data array is passed in, then that is used instead of self._data.
        This behavior is useful for subclasses.
        """
        if data is None:
            data = self.get_data()

        d_min = np.nanmin(data)
        d_max = np.nanmax(data)
        self._cached_bounds = (d_min, d_max)
