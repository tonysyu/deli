from numpy.testing import assert_allclose

from deli.layout.bounding_box import BoundingBox
from deli.layout.grid_layout import XGridLayout, YGridLayout


UNIT_BBOX = BoundingBox.from_extents(0, 0, 1, 1)


def assert_grid_within_limits(grid, min_offset, max_offset):
    assert_allclose(grid.axial_limits, (min_offset, max_offset))
    assert grid.axial_offsets.min() >= min_offset
    assert grid.axial_offsets.max() <= max_offset


def test_x_grid_layout():
    grid = XGridLayout(data_bbox=UNIT_BBOX)
    assert_allclose(grid.axial_limits, (0, 1))
    assert_grid_within_limits(grid, 0, 1)


def test_x_grid_update():
    bbox = UNIT_BBOX.copy()
    grid = XGridLayout(data_bbox=bbox)
    # Altering the x_limits should alter the grid layout.
    bbox.x_limits = (0.1, 0.2)
    assert_grid_within_limits(grid, 0.1, 0.2)


def test_y_grid_update():
    bbox = UNIT_BBOX.copy()
    grid = YGridLayout(data_bbox=bbox)
    # Altering the y_limits should alter the grid layout.
    bbox.y_limits = (0.1, 0.2)
    assert_grid_within_limits(grid, 0.1, 0.2)
