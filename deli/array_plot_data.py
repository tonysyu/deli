""" Defines ArrayPlotData.
"""
from traits.api import Dict

from .abstract_plot_data import AbstractPlotData


class ArrayPlotData(AbstractPlotData):
    """ A PlotData implementation class that handles a list of Numpy arrays
    (or a 2-D Numpy array).

    By default, it doesn't allow its input data to be modified by downstream
    components or interactors.
    """

    # Map of names to arrays.
    arrays = Dict

    writable = True

    def __init__(self, *data, **kw):
        super(AbstractPlotData, self).__init__()
        self._update_data(kw)
        data = dict(zip(self._generate_names(len(data)), data))
        self._update_data(data)

    def get_data(self, name):
        """ Returns the array associated with *name*.

        Implements AbstractDataSource.
        """
        return self.arrays.get(name, None)

    def set_data(self, name, new_data, generate_name=False):
        """ Sets the specified array as the value for either the specified
        name or a generated name.

        If the instance's `writable` attribute is True, then this method sets
        the data associated with the given name to the new value, otherwise it
        does nothing.

        Parameters
        ----------
        name : string
            The name of the array whose value is to be set.
        new_data : array
            The array to set as the value of *name*.
        generate_name : Boolean
            If True, a unique name of the form 'seriesN' is created for the
            array, and is used in place of *name*. The 'N' in 'seriesN' is
            one greater the largest N already used.

        Returns
        -------
        The name under which the array was set.

        """
        self.update_data({name: new_data})
        return name


    def update_data(self, *args, **kwargs):
        """ Sets the specified array as the value for either the specified
        name or a generated name.

        Implements AbstractPlotData's update_data() method.  This method has
        the same signature as the dictionary update() method.

        """
        data = dict(*args, **kwargs)
        event = {}
        for name in data:
            event.setdefault('added', []).append(name)

        self._update_data(data)
        self.data_changed = event

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------    

    def _generate_names(self, n):
        """ Generate n new names
        """
        max_index = max(self._generate_indices())
        names = ["series{0:d}".format(n)
                for n in range(max_index+1, max_index+n+1)]
        return names

    def _generate_indices(self):
        """ Generator that yields all integers that match "series%d" in keys
        """
        yield 0 # default minimum

    def _update_data(self, data):
        """ Update the array, ensuring that data is an array
        """
        # note that this call modifies data, but that's OK since the callers
        # all create the dictionary that they pass in
        for name, value in data.items():
            data[name] = value

        self.arrays.update(data)
