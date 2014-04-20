""" Defines the ArrayDataSource class."""
import numpy as np

from traits.api import Tuple

from .base import NumericalSequenceTrait
from .abstract_data_source import AbstractDataSource


class ArrayDataSource(AbstractDataSource):
    """ A data source representing a single, continuous array of numerical data.
    """

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

    def __init__(self, data=np.array([]), **kw):
        AbstractDataSource.__init__(self, **kw)
        self.set_data(data)

    def set_data(self, newdata):
        """ Sets the data, and optionally the sort order, for this data source.

        Parameters
        ----------
        newdata : array
            The data to use.
        sort_order : SortOrderTrait
            The sort order of the data
        """
        self._data = newdata
        self.data_changed = True

    #------------------------------------------------------------------------
    # AbstractDataSource interface
    #------------------------------------------------------------------------

    def get_data(self):
        """ Returns the data for this data source, or 0.0 if it has no data.

        Implements AbstractDataSource.
        """
        return self._data
