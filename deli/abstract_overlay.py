""" Abstract base class for plot decorators and overlays.

This class is primarily used so that tools can easily distinguish between
data-related plot items and the decorators on them.
"""
from traits.api import Instance

from .core.component import Component
from .plot_component import PlotComponent


class AbstractOverlay(PlotComponent):
    """ The base class for overlays and underlays of the plot area. """

    # The component that this object overlays. This can be None. By default, if
    # this object is called to draw(), it tries to render onto this component.
    component = Instance(Component)

    # The default layer that this component draws into.
    draw_layer = "overlay"

    # The background color (overrides PlotComponent).
    bgcolor = "transparent"

    def __init__(self, component=None, *args, **kw):
        if component is not None:
            self.component = component
        super(AbstractOverlay, self).__init__(*args, **kw)
