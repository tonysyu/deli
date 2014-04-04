""" Defines the base class for plot data.
"""
from traits.api import Bool, Event, HasTraits


class AbstractPlotData(HasTraits):
    """ Defines the interface for data providers to Plot. """

    data_changed = Event

    writable = Bool(True)

    selectable = Bool(True)
