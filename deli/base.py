"""
Defines basic traits and functions for the data model.
"""
from numpy import empty

from traits.api import CArray, Trait


# A single array of numbers.
NumericalSequenceTrait = Trait(None, None, CArray(value=empty(0)))
