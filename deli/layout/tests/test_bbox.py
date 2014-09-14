from contextlib import contextmanager
from unittest import TestCase

from numpy.testing import assert_allclose, assert_raises

from traits.api import TraitError
from traits.testing.unittest_tools import UnittestTools

from deli.layout.bounding_box import BoundingBox


#--------------------------------------------------------------------------
#  Utilities and test data
#--------------------------------------------------------------------------

SMALL = BoundingBox.from_extents(1, 2, 3, 4)
MEDIUM = BoundingBox.from_extents(10, 20, 30, 40)
LARGE = BoundingBox.from_extents(100, 200, 300, 400)


def assert_setattr_raises(obj, attr_name, value=None):
    assert_raises(TraitError, setattr, obj, attr_name, value)


#--------------------------------------------------------------------------
#  Test bounds accessors
#--------------------------------------------------------------------------

def test_x_and_y():
    bbox = BoundingBox.from_extents(1, 2, 3, 4)
    assert_allclose(bbox.x0, 1)
    assert_allclose(bbox.y0, 2)
    assert_allclose(bbox.x1, 3)
    assert_allclose(bbox.y1, 4)


def test_x_and_y_limits():
    bbox = BoundingBox.from_extents(1, 2, 3, 4)
    assert_allclose(bbox.x_limits, (1, 3))
    assert_allclose(bbox.y_limits, (2, 4))


def test_rect():
    bbox = BoundingBox.from_extents(1, 2, 3, 4)
    assert_allclose(bbox.rect, (1, 2, 2, 2))


def test_width_and_height():
    bbox = BoundingBox.from_rect(1, 2, 10, 20)
    assert_allclose(bbox.width, 10)
    assert_allclose(bbox.height, 20)

    assert_setattr_raises(bbox, 'width')
    assert_setattr_raises(bbox, 'height')


#--------------------------------------------------------------------------
#  Test Properties
#--------------------------------------------------------------------------

class TestSetProperties(TestCase, UnittestTools):

    def setUp(self):
        self.bbox = BoundingBox.from_extents(1, 2, 3, 4)

    @contextmanager
    def assert_bbox_updated(self, count=1):
        with self.assertTraitChanges(self.bbox, 'updated', count=1):
            yield

    def test_x_and_y_updated(self):
        with self.assert_bbox_updated():
            self.bbox.x0 = 10
        assert_allclose(self.bbox.x0, 10)

        with self.assert_bbox_updated():
            self.bbox.x1 = 30
        assert_allclose(self.bbox.x1, 30)

        with self.assert_bbox_updated():
            self.bbox.y0 = 20
        assert_allclose(self.bbox.y0, 20)

        with self.assert_bbox_updated():
            self.bbox.y1 = 40
        assert_allclose(self.bbox.y1, 40)

    def test_x_and_y_limits_updated(self):
        with self.assert_bbox_updated():
            self.bbox.x_limits = (10, 30)
        assert_allclose(self.bbox.x_limits, (10, 30))

        with self.assert_bbox_updated():
            self.bbox.y_limits = (20, 40)
        assert_allclose(self.bbox.y_limits, (20, 40))
