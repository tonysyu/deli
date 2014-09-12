"""Helper functions for a simple layout algorithm.
"""

def simple_container_do_layout(container, components=None):
    """ Adjust layout so container stretches to window size.
    """
    if components is None:
        components = container.components

    width = container.width
    height = container.height
    apply_size_to_all_components((width, height), container, components)


def apply_size_to_all_components(size, container, components):
    for component in components:
        component.origin = [0, 0]
        component.size = size
