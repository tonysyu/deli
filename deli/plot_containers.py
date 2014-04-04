""" Defines various plot container classes, including stacked, grid, and
overlay.
"""
from traits.api import Instance, Tuple
from enable.simple_layout import (simple_container_get_preferred_size,
                                  simple_container_do_layout)

from .base_plot_container import BasePlotContainer
from .plot_component import DEFAULT_DRAWING_ORDER


__all__ = ["OverlayPlotContainer"]


class OverlayPlotContainer(BasePlotContainer):
    """
    A plot container that stretches all its components to fit within its
    space.  All of its components must therefore be resizable.
    """

    draw_order = Instance(list, args=(DEFAULT_DRAWING_ORDER,))

    # Do not use an off-screen backbuffer.
    use_backbuffer = False

    # Cache (width, height) of the container's preferred size.
    _cached_preferred_size = Tuple

    def get_preferred_size(self, components=None):
        """ Returns the size (width,height) that is preferred for this component.

        Overrides PlotComponent
        """
        return simple_container_get_preferred_size(self, components=components)

    def _do_layout(self):
        """ Actually performs a layout (called by do_layout()).
        """
        simple_container_do_layout(self)
