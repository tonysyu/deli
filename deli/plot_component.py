""" Defines the PlotComponent class.
"""
from traits.api import Instance

from .core.component import Component
from .layout.bounding_box import BoundingBox


class PlotComponent(Component):

    #--------------------------------------------------------------------------
    #  Bounding box
    #--------------------------------------------------------------------------

    #: Bounding box in screen coordinates
    screen_bbox = Instance(BoundingBox)

    def _screen_bbox_default(self):
        return BoundingBox.from_extents(self.x, self.y, self.x2, self.y2)

    def _bounds_changed(self, old, new):
        super(PlotComponent, self)._bounds_changed(old, new)
        self._update_bbox()

    def _update_bbox(self):
        self.screen_bbox.bounds = (self.x, self.y, self.width, self.height)
