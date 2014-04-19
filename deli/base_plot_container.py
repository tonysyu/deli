""" Defines the BasePlotContainer class.
"""
from enable.api import Container
from traits.api import Instance, Str, Tuple

from .layout.bounding_box import BoundingBox
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

    #--------------------------------------------------------------------------
    #  Bounding box
    #--------------------------------------------------------------------------

    #: Bounding box in screen coordinates
    screen_bbox = Instance(BoundingBox)

    def _screen_bbox_default(self):
        return BoundingBox.from_extents(self.x, self.y, self.x2, self.y2)

    def _bounds_changed(self, old, new):
        super(BasePlotContainer, self)._bounds_changed(old, new)
        self._update_bbox()

    def _position_changed(self, old, new):
        super(BasePlotContainer, self)._position_changed(old, new)
        self._update_bbox()

    def _update_bbox(self):
        self.screen_bbox.bounds = (self.x, self.y, self.width, self.height)
        self.invalidate_draw()
