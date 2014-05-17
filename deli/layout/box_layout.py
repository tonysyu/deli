"""Helper functions for a simple layout algorithm.
"""

def enforce_screen_aspect_ratio(container, components=None):
    """ Adjust the size of the component to match the aspect ratio. """
    if components is None:
        components = container.components

    ratio = container.aspect_ratio
    if ratio == 0:
        container.width = 0

    old_width, old_height = container.bounds
    desired_width = (ratio or 0) * old_height
    if desired_width == 0 or int(old_width) == int(desired_width):
        simple_container_do_layout(container, components=components)
        return

    old_ratio = old_width / float(old_height)
    new_position = container.position[:]
    if ratio > old_ratio:
        # Increase aspect-ratio: Use the width and compute a smaller height.
        new_width = old_width
        new_height = new_width / ratio
        if container.auto_center:
            new_position[1] += (old_height - new_height) / 2.0
    else:
        # Decrease aspect-ratio: Use the height and compute a smaller width.
        new_height = old_height
        new_width = new_height * ratio
        if container.auto_center:
            new_position[0] += (old_width - new_width) / 2.0

    new_size = (new_width, new_height)
    apply_size_to_all_components(new_size, container, components)

    # Fixing the aspect ratio requires changes to the default padding, so we
    # need to update the container geometry.
    container.position = new_position
    container.bounds = new_size


def simple_container_do_layout(container, components=None):
    """ Adjust layout so container stretches to window bounds (minus padding).
    """
    if components is None:
        components = container.components

    width = container.width
    height = container.height
    apply_size_to_all_components((width, height), container, components)


def apply_size_to_all_components(size, container, components, position=None):
    for component in components:
        if hasattr(container, '_should_layout'):
            if not container._should_layout(component):
                continue

        component.outer_position = [0, 0]
        component.outer_bounds = size
