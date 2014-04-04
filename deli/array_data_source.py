""" Defines the ArrayDataSource class."""
from numpy import array, nanargmin, nanargmax, ndarray

from traits.api import Any, Tuple

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

    # The index of the (first) minimum value in self._data
    _min_index = Any

    # The index of the (first) maximum value in self._data
    _max_index = Any

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def __init__(self, data=array([]), sort_order="none", **kw):
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
        # TODO: as an optimization, perhaps create and cache a sorted
        #       version of the dataset?

        if data is None:
            # Several sources weren't setting the _data attribute, so we
            # go through the interface.  This seems like the correct thing
            # to do anyway... right?
            #data = self._data
            data = self.get_data()

        self._min_index = nanargmin(data.view(ndarray))
        self._max_index = nanargmax(data.view(ndarray))

        self._cached_bounds = (data[self._min_index],
                               data[self._max_index])
