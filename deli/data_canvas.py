import numpy as np

from enable.api import Container
from traits.api import Callable, Instance, Property, Str

from .layout.bbox_transform import BboxTransform
from .layout.bounding_box import BoundingBox
from .layout.box_layout import enforce_screen_aspect_ratio
from .plot_component import DEFAULT_DRAWING_ORDER


class DataCanvas(Container):
    """ Represents a mapping from 2-D data space into 2-D screen space.

    It can house plots and other plot components, and otherwise behaves
    just like a normal Container.
    """

    draw_order = Instance(list, args=(DEFAULT_DRAWING_ORDER,))
    draw_layer = Str("plot")

    # Do not use an off-screen backbuffer.
    use_backbuffer = False

    #--------------------------------------------------------------------------
    #  Bounding box
    #--------------------------------------------------------------------------

    #: Bounding box in screen coordinates
    screen_bbox = Instance(BoundingBox)

    # The bounding box containing data added to plot.
    data_bbox = Instance(BoundingBox)

    def _screen_bbox_default(self):
        return BoundingBox.from_extents(self.x, self.y, self.x2, self.y2)

    def _data_bbox_default(self):
        return BoundingBox.from_extents(np.inf, np.inf, -np.inf, -np.inf)

    def _bounds_changed(self, old, new):
        super(DataCanvas, self)._bounds_changed(old, new)
        self._update_bbox()

    def _position_changed(self, old, new):
        super(DataCanvas, self)._position_changed(old, new)
        self._update_bbox()

    def _update_bbox(self):
        self.screen_bbox.bounds = (self.x, self.y, self.width, self.height)
        self.invalidate_draw()

    #--------------------------------------------------------------------------
    #  Transformations
    #--------------------------------------------------------------------------

    #: Transform from data space to screen space.
    data_to_screen = Instance(BboxTransform)

    #: Transform from data space to screen space.
    screen_to_data = Property(Instance(BboxTransform),
                              depends_on='data_to_screen')

    def _data_to_screen_default(self):
        return BboxTransform(self.data_bbox, self.screen_bbox)

    def _get_screen_to_data(self):
        return self.data_to_screen.inverted()

    #--------------------------------------------------------------------------
    #  Layout
    #--------------------------------------------------------------------------

    calculate_layout = Callable

    def _calculate_layout_default(self):
        return enforce_screen_aspect_ratio

    def _do_layout(self):
        """ Adjust component layout (called by do_layout()). """
        self.calculate_layout(self)
