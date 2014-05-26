from deli.core.constraints_container import ConstraintsContainer
from deli.testing.constraints import assert_matches_size


WIDTH = 100
HEIGHT = 200


def container_with_default_size():
    container = ConstraintsContainer()
    container.layout_constraints = [
        container.layout_width == WIDTH,
        container.layout_height == HEIGHT
    ]
    return container


def test_layout_size():
    container = container_with_default_size()
    assert_matches_size(container, (WIDTH, HEIGHT))


def fill_container(component):
    """ Stretch a child component to fill its parent container.

    Note that the layout is solved bottom up so, if the component's
    `share_layout` is not set to True, the parent container won't have a size.
    """
    if not component.share_layout:
        raise RuntimeError("Component must have `share_layout = True`")
    return [component.left == component.container.left,
            component.right == component.container.right,
            component.top == component.container.top,
            component.bottom == component.container.bottom]


def test_child_container_fills_parent_container():
    # Note that the `share_layout` flag allows the parent to dictate the size
    # of the child. Otherwise, the child constraints are solved first.
    child = ConstraintsContainer(share_layout=True)
    child.layout_constraints = fill_container

    parent = container_with_default_size()
    parent.add(child)

    # Check that child doesn't change parent container's size.
    assert_matches_size(parent, (WIDTH, HEIGHT))
    # Check that child size matches parent.
    assert_matches_size(child, (WIDTH, HEIGHT))
