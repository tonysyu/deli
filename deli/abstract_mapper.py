""" Defines the base class for mappings.
"""
from traits.api import Event, HasStrictTraits


class AbstractMapper(HasStrictTraits):

    updated = Event
