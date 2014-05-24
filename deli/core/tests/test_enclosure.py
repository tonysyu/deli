from deli.core.component import Component
from deli.core.constraints_container import ConstraintsContainer
from deli.testing.constraints import assert_matches_size


WIDTH = 100
HEIGHT = 200


def enclosure(container):
    """ Layout constraint to ensure a container surrounds its child components.
    """
    constraints = []
    for c in container.components:
        constraints.extend([container.left <= c.left,
                            container.right >= c.right,
                            container.top >= c.top,
                            container.bottom <= c.bottom])
    return constraints


def _test_parent_stretches_around_child(child, size):
    parent = ConstraintsContainer()
    parent.layout_constraints = enclosure
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
