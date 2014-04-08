"""
Defines the AbstractDataSource class.
"""
from traits.api import Event, HasStrictTraits


class AbstractDataSource(HasStrictTraits):

    data_changed = Event
