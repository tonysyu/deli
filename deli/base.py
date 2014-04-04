"""
Defines basic traits and functions for the data model.
"""
from numpy import concatenate, empty, nonzero, ndarray

from traits.api import CArray, Enum, Trait


# A single array of numbers.
NumericalSequenceTrait = Trait(None, None, CArray(value=empty(0)))

# A sequence of pairs of numbers, i.e., an Nx2 array.
PointTrait = Trait(None, None, CArray(value=empty(0)))

# An NxM array of numbers.
ImageTrait = Trait(None, None, CArray(value=empty(0)))

# An 3D array of numbers of shape (Nx, Ny, Nz)
CubeTrait = Trait(None, None, CArray(value=empty(0)))


# This enumeration lists the supported mathematical coordinate.
DimensionTrait = Enum("scalar", "point", "image", "cube")

# Linear sort order.
SortOrderTrait = Enum("ascending", "descending", "none")


def right_shift(ary, newval):
    "Returns a right-shifted version of *ary* with *newval* inserted on the left."
    return concatenate([[newval], ary[:-1]])

def left_shift(ary, newval):
    "Returns a left-shifted version of *ary* with *newval* inserted on the right."
    return concatenate([ary[1:], [newval]])

def arg_find_runs(int_array, order='ascending'):
    """
    Like find_runs(), but returns a list of tuples indicating the start and
    end indices of runs in the input *int_array*.
    """
    assert len(int_array.shape)==1, "find_runs() requires a 1D integer array."
    rshifted = right_shift(int_array, int_array[0]).view(ndarray)
    start_indices = concatenate([[0], nonzero(int_array - (rshifted))[0]])
    end_indices = left_shift(start_indices, len(int_array))
    return zip(start_indices, end_indices)
