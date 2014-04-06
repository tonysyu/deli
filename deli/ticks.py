""" Tick generator classes and helper functions for calculating axis
tick-related values (i.e., bounds and intervals).

"""
from numpy import (arange, argsort, array, float64, floor, log10, minimum,
                   newaxis, shape)

from traits.api import HasStrictTraits


class AbstractTickGenerator(HasStrictTraits):
    pass


class DefaultTickGenerator(AbstractTickGenerator):
    """ An implementation of AbstractTickGenerator that simply uses the
    auto_ticks() and log_auto_ticks() functions.
    """
    def get_ticks(self, bounds_low, bounds_high, interval):
        ticks = auto_ticks(bounds_low, bounds_high, interval)
        return array(ticks, float64)


def auto_ticks(bound_low, bound_high, tick_interval):
    """ Finds locations for axis tick marks.

        Calculates the locations for tick marks on an axis. The *bound_low*,
        *bound_high*, and *tick_interval* parameters specify how the axis end
        points and tick interval are calculated.

        Parameters
        ----------
        bound_low, bound_high : 'auto', 'fit', or a number.
            The lower and upper bounds of the axis. If the value is a number,
            that value is used for the corresponding end point. If the value is
            'auto', then the end point is calculated automatically. If the
            value is 'fit', then the axis bound is set to the corresponding
            *data_low* or *data_high* value.
        tick_interval : can be 'auto' or a number
            If the value is a positive number, it specifies the length
            of the tick interval; a negative integer specifies the
            number of tick intervals; 'auto' specifies that the number and
            length of the tick intervals are automatically calculated, based
            on the range of the axis.

        Returns
        -------
        An array of tick mark locations. The first and last tick entries are the
        axis end points.
    """
    lower = float(bound_low)
    upper = float(bound_high)

    tick_interval = auto_interval( lower, upper )

    # Compute the range of ticks values:
    start = floor(lower / tick_interval) * tick_interval
    end = floor(upper / tick_interval) * tick_interval

    if upper > end:
        end += tick_interval
    ticks = arange( start, end + (tick_interval / 2.0), tick_interval )

    return [tick for tick in ticks if tick >= bound_low and tick <= bound_high]


def auto_interval(data_low, data_high):
    """ Calculates the tick interval for a range.

        The boundaries for the data to be plotted on the axis are::

            data_bounds = (data_low,data_high)

        The function chooses the number of tick marks, which can be between
        3 and 9 marks (including end points), and chooses tick intervals at
        1, 2, 2.5, 5, 10, 20, ...

        Returns
        -------
        interval : float
            tick mark interval for axis
    """
    range = float( data_high ) - float( data_low )

    # We'll choose from between 2 and 8 tick marks.
    # Preference is given to more ticks:
    #   Note reverse order and see kludge below...
    divisions = arange( 8.0, 2.0, -1.0 ) # ( 7, 6, ..., 3 )

    # Calculate the intervals for the divisions:
    candidate_intervals = range / divisions

    # Get magnitudes and mantissas for each candidate:
    magnitudes = 10.0 ** floor( log10( candidate_intervals ) )
    mantissas  = candidate_intervals / magnitudes

    # List of "pleasing" intervals between ticks on graph.
    # Only the first magnitude are listed, higher mags others are inferred:
    magic_intervals = array( ( 1.0, 2.0, 2.5, 5.0, 10.0 ) )

    # Calculate the absolute differences between the candidates
    # (with magnitude removed) and the magic intervals:
    differences = abs( magic_intervals[:,newaxis] - mantissas )

    # Find the division and magic interval combo that produce the
    # smallest differences:

    # KLUDGE: 'argsort' doesn't preserve the order of equal values,
    # so we subtract a small, index dependent amount from each difference
    # to force correct ordering.
    sh    = shape( differences )
    small = 2.2e-16 * arange( sh[1] ) * arange( sh[0] )[:,newaxis]
    small = small[::-1,::-1] #reverse the order
    differences = differences - small

    # ? Numeric should allow keyword "axis" ? comment out for now
    #best_mantissa = minimum.reduce(differences,axis=0)
    #best_magic = minimum.reduce(differences,axis=-1)
    best_mantissa  = minimum.reduce( differences,  0 )
    best_magic     = minimum.reduce( differences, -1 )
    magic_index    = argsort( best_magic )[0]
    mantissa_index = argsort( best_mantissa )[0]

    # The best interval is the magic_interval multiplied by the magnitude
    # of the best mantissa:
    interval  = magic_intervals[ magic_index ]
    magnitude = magnitudes[ mantissa_index ]
    result    = interval * magnitude
    return result
