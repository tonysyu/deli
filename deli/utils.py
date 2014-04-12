import numpy as np


def switch_trait_handler(old, new, observed_trait_name, handler):
    """Move handler from one `HasTraits` object to another.

    Parameters
    ----------
    old, new : HasTraits instance
        HasTraits objects with a trait that's being observed.
    observed_trait_name : str
        Observed trait on `old` and `new` `HasTraits` objects.
    handler : function
        The handler function that's fired when the oberved trait changes.
    """
    if old is not None:
        old.on_trait_change(handler, observed_trait_name, remove=True)
    if new is not None:
        new.on_trait_change(handler, observed_trait_name)


def hline_segments(y, x_lo, x_hi):
    """ Return start and end points for horizontal line segments.

    Parameters
    ----------
    y : float or array
        Vertical positions for horizontal lines.
    x_lo, x_hi : float or array
        End points for horizontal lines.
    """
    y, x_lo, x_hi = np.broadcast_arrays(y, x_lo, x_hi)
    starts = np.column_stack((x_lo, y))
    ends = np.column_stack((x_hi, y))
    return starts, ends


def vline_segments(x, y_lo, y_hi):
    """ Return start and end points for vertical line segments.

    Parameters
    ----------
    x : float or array
        Horizontal positions for vertical lines.
    y_lo, y_hi : float or array
        End points for vertical lines.
    """
    x, y_lo, y_hi = np.broadcast_arrays(x, y_lo, y_hi)
    starts = np.column_stack((x, y_lo))
    ends = np.column_stack((x, y_hi))
    return starts, ends
