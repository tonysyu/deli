"""
Defines the base class for data ranges.
"""
from traits.api import Float, HasStrictTraits, Instance, List, Trait

from .abstract_data_source import AbstractDataSource


class AbstractDataRange(HasStrictTraits):

    # The list of data sources to which this range responds.
    sources = List(Instance(AbstractDataSource))

    low = Float(0.0)

    high = Float(1.0)

    low_setting = Trait('auto', 'auto', Float)

    high_setting = Trait('auto', 'auto', Float)
