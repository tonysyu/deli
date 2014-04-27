""" Defines the DataView class, and associated property traits and property
functions.
"""
import numpy as np

from traits.api import Bool, Instance

from .axis import BaseAxis, XAxis, YAxis
from .grid import BaseGrid, XGrid, YGrid
from .layout.bbox_transform import BboxTransform
from .layout.bounding_box import BoundingBox
from .plot_containers import OverlayPlotContainer


class DataView(OverlayPlotContainer):
    """ Represents a mapping from 2-D data space into 2-D screen space.

    It can house renderers and other plot components, and otherwise behaves
    just like a normal PlotContainer.
    """

    # The bounding box containing data added to plot.
    data_bbox = Instance(BoundingBox)

    def _data_bbox_default(self):
        return BoundingBox.from_extents(np.inf, np.inf, -np.inf, -np.inf)

    #: Transform from data space to screen space.
    data_to_screen = Instance(BboxTransform)

    def _data_to_screen_default(self):
        return BboxTransform(self.data_bbox, self.screen_bbox)

    #------------------------------------------------------------------------
    # Axis and Grids
    #------------------------------------------------------------------------

    # The horizontal axis.
    x_axis = Instance(BaseAxis)

    # The vertical axis.
    y_axis = Instance(BaseAxis)

    # The grid that intersects the x-axis, i.e., a set of vertical lines.
    x_grid = Instance(BaseGrid)

    # The grid that intersects the y-axis, i.e., a set of horizontal lines.
    y_grid = Instance(BaseGrid)

    # Whether to automatically create the x_axis and y_axis if they were not
    # already set by the caller.
    auto_axis = Bool(True)

    # Whether to automatically create the x_grid and y_grid if they were not
    # already set by the caller.
    auto_grid = Bool(True)

    #------------------------------------------------------------------------
    # Appearance
    #------------------------------------------------------------------------

    bgcolor = "white"

    # Padding defaults.
    padding_top = 50
    padding_bottom = 50
    padding_left = 50
    padding_right = 50

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def __init__(self, **kwtraits):
        super(DataView, self).__init__(**kwtraits)
        self._init_components()

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _init_components(self):
        if not self.x_grid and self.auto_grid:
            self.x_grid = XGrid(component=self)
        if not self.y_grid and self.auto_grid:
            self.y_grid = YGrid(component=self)

        if not self.x_axis and self.auto_axis:
            self.x_axis = XAxis(component=self)

        if not self.y_axis and self.auto_axis:
            self.y_axis = YAxis(component=self)

    #-------------------------------------------------------------------------
    # Event handlers
    #-------------------------------------------------------------------------

    def _x_grid_changed(self, old, new):
        self._underlay_change_helper(old, new)

    def _y_grid_changed(self, old, new):
        self._underlay_change_helper(old, new)

    def _x_axis_changed(self, old, new):
        self._underlay_change_helper(old, new)

    def _y_axis_changed(self, old, new):
        self._underlay_change_helper(old, new)

    def _underlay_change_helper(self, old, new):
        if old in self.underlays:
            self.underlays.remove(old)
        if new is not None:
            self.underlays.append(new)

    def _overlay_change_helper(self, old, new):
        if old in self.overlays:
            self.overlays.remove(old)
        if new is not None:
            self.overlays.append(new)
