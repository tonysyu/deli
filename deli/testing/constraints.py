from numpy.testing import assert_equal


def assert_matches_size(component, size):
    assert_equal(component.layout_width.value, size[0])
    assert_equal(component.layout_height.value, size[1])
