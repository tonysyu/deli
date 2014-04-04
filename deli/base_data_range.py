"""
Defines the BaseDataRange class.
"""
from abstract_data_range import AbstractDataRange


class BaseDataRange(AbstractDataRange):
    """ Ranges represent sub-regions of data space. """

    def add(self, *datasources):
        """ Convenience method to add a data source. """
        for datasource in datasources:
            if datasource not in self.sources:
                self.sources.append(datasource)
