"""
Defines the base class for data ranges.
"""
from traits.api import Event, Float, HasStrictTraits, Instance, List, Trait

from .abstract_data_source import AbstractDataSource


class AbstractDataRange(HasStrictTraits):
    """ Ranges represent sub-regions of data space. """

    # The list of data sources to which this range responds.
    sources = List(Instance(AbstractDataSource))

    low = Float(0.0)

    high = Float(1.0)

    low_setting = Trait('auto', 'auto', Float)

    high_setting = Trait('auto', 'auto', Float)

    updated = Event

    def add(self, *datasources):
        """ Convenience method to add a data source. """
        for datasource in datasources:
            if datasource not in self.sources:
                self.sources.append(datasource)
