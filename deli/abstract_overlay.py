""" Abstract base class for plot decorators and overlays.

This class is primarily used so that tools can easily distinguish between
data-related plot items and the decorators on them.
"""
from traits.api import Instance

from .core.component import Component


class AbstractOverlay(Component):
    """ The base class for overlays and underlays of the plot area. """

    # The component that this object overlays. This can be None. By default, if
    # this object is called to draw(), it tries to render onto this component.
    component = Instance(Component)
