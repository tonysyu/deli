""" Defines the BasePlotContainer class.
"""
from enable.api import Container
from traits.api import Instance, Str, Tuple

from .plot_component import DEFAULT_DRAWING_ORDER


class BasePlotContainer(Container):
    """
    A container for PlotComponents that conforms to being laid out by
    PlotFrames.  Serves as the base class for other PlotContainers.

    PlotContainers define a layout, i.e., a spatial relationship between
    their contained components.  (BasePlotContainer doesn't define one,
    but its various subclasses do.)

    BasePlotContainer is a subclass of Enable Container, so it is possible to
    insert Enable-level components into it.  However, because Enable
    components don't have the correct interfaces to participate in layout,
    the visual results will probably be incorrect.
    """

    # Redefine the container layers to name the main layer as "plot" instead
    # of the Enable default of "mainlayer"
    container_under_layers = Tuple("background", "image", "underlay", "plot")

    draw_order = Instance(list, args=(DEFAULT_DRAWING_ORDER,))
    draw_layer = Str("plot")
