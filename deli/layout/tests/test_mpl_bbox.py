import numpy as np
from numpy.testing import assert_allclose

from matplotlib.transforms import Bbox, BboxTransform


# -------------------------------------------------------------------------
#  Utilities and test data
# -------------------------------------------------------------------------

SMALL = Bbox.from_extents(1, 2, 3, 4)
MEDIUM = Bbox.from_extents(10, 20, 30, 40)
LARGE = Bbox.from_extents(100, 200, 300, 400)


def _test_transform_corners(transform_instance, bbox0, bbox1):
    transform = transform_instance.transform
    assert_allclose(transform((bbox0.x0, bbox0.y0)), (bbox1.x0, bbox1.y0))
    assert_allclose(transform((bbox0.x1, bbox0.y0)), (bbox1.x1, bbox1.y0))
    assert_allclose(transform((bbox0.x0, bbox0.y1)), (bbox1.x0, bbox1.y1))
    assert_allclose(transform((bbox0.x1, bbox0.y1)), (bbox1.x1, bbox1.y1))


# -------------------------------------------------------------------------
#  Basic tests
# -------------------------------------------------------------------------

def test_basic():
    _test_transform_corners(BboxTransform(SMALL, LARGE), SMALL, LARGE)


def test_inverted():
    inv = BboxTransform(SMALL, LARGE).inverted()
    _test_transform_corners(inv, LARGE, SMALL)


def test_composite():
    small_to_medium = BboxTransform(SMALL, MEDIUM)
    medium_to_large = BboxTransform(MEDIUM, LARGE)
    composite = small_to_medium + medium_to_large

    _test_transform_corners(composite, SMALL, LARGE)


# -------------------------------------------------------------------------
#  Test updates
# -------------------------------------------------------------------------

def test_updated():
    # Copy this bbox, since we're going to modify it later.
    large = Bbox.from_bounds(*LARGE.bounds)
    small_to_medium = BboxTransform(SMALL, MEDIUM)
    small_to_large = BboxTransform(SMALL, large)

    # Sanity check before manipulating bounds.
    _test_transform_corners(small_to_large, SMALL, LARGE)
    _test_transform_corners(small_to_medium, SMALL, MEDIUM)

    # Update bounds of large bbox and test updated transform.
    large.bounds = MEDIUM.bounds
    _test_transform_corners(small_to_large, SMALL, MEDIUM)


def test_update_from_data():
    small = Bbox.from_bounds(*SMALL.bounds)
    # small.update_from_data(np.array([3]), np.array([3]))
    assert_allclose(small.x0, SMALL.x0)
    assert_allclose(small.x1, SMALL.x1)


# -------------------------------------------------------------------------
#  Test transform inputs
# -------------------------------------------------------------------------

def test_transform_list_of_points():
    trans = BboxTransform(SMALL, LARGE)
    result = trans.transform([(SMALL.x0, SMALL.y0),
                              (SMALL.x1, SMALL.y1)])
    expected = [(LARGE.x0, LARGE.y0),
                (LARGE.x1, LARGE.y1)]
    assert_allclose(result, expected)


def test_transform_array():
    trans = BboxTransform(SMALL, LARGE)
    result = trans.transform(np.array([(SMALL.x0, SMALL.y0),
                                       (SMALL.x1, SMALL.y1)]))
    expected = [(LARGE.x0, LARGE.y0),
                (LARGE.x1, LARGE.y1)]
    assert_allclose(result, expected)
