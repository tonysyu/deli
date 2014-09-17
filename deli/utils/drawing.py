import numpy as np


def broadcast_points(x, y):
    """ Return array of x- and y-points from x and y arrays or scalars.

    Parameters
    ----------
    x, y : (N,) array or scalar
        Scalar values will be

    Returns
    -------
    points : (N, 2) array
        x/y points with (x, y) values on each row.
    """
    return np.transpose(np.broadcast_arrays(x, y))


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
