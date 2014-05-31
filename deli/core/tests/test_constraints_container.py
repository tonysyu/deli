from numpy.testing import assert_array_equal

from deli.core.component import Component
from deli.core.constraints_container import ConstraintsContainer
from deli.testing.constraints import assert_matches_size


WIDTH = 100
HEIGHT = 200
SIZE = (WIDTH, HEIGHT)


def test_child_container_fills_parent_container():
    parent = ConstraintsContainer(size=SIZE)
    child = ConstraintsContainer()
    parent.add(child)
    # XXX: For some reason, the layout width/height is temporarily set to the
    # bounds-size, but it gets changed before access.
    assert_array_equal(parent.size, SIZE)
    assert_array_equal(child.size, SIZE)


def _test_parent_stretches_around_child(child, size):
    parent = ConstraintsContainer()
    parent.add(child)

    # Check that parent doesn't change child container's size.
    assert_matches_size(child, size)
    # Check that parent size matches child.
    assert_matches_size(parent, size)


def test_parent_stretches_around_child_container():
    child = ConstraintsContainer()
    child.layout_size_hint = (WIDTH, HEIGHT)
    _test_parent_stretches_around_child(child, (WIDTH, HEIGHT))


def test_parent_stretches_around_child_component():
    child = Component()
    child.layout_size_hint = (WIDTH, HEIGHT)
    _test_parent_stretches_around_child(child, (WIDTH, HEIGHT))
