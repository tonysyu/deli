""" Defines the DataCanvas class, and associated property traits and property
functions.
"""
import numpy as np

from traits.api import Bool, Instance, Property

from .axis import BaseAxis, XAxis, YAxis
from .grid import BaseGrid, XGrid, YGrid
from .layout.bbox_transform import BboxTransform
from .layout.bounding_box import BoundingBox
from .plot_containers import OverlayPlotContainer


def replace_in_list(a_list, old, new):
    if old in a_list:
        a_list.remove(old)
    if new is not None:
        a_list.append(new)


class DataCanvas(OverlayPlotContainer):
    """ Represents a mapping from 2-D data space into 2-D screen space.

    It can house plots and other plot components, and otherwise behaves
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

    #: Transform from data space to screen space.
    screen_to_data = Property(Instance(BboxTransform),
                              depends_on='data_to_screen')

    def _get_screen_to_data(self):
        return self.data_to_screen.inverted()

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
        super(DataCanvas, self).__init__(**kwtraits)
        self._init_components()

    #-------------------------------------------------------------------------
    # Event handlers
    #-------------------------------------------------------------------------

    def _x_grid_changed(self, old, new):
        self._replace_underlay(old, new)

    def _y_grid_changed(self, old, new):
        self._replace_underlay(old, new)

    def _x_axis_changed(self, old, new):
        self._replace_underlay(old, new)

    def _y_axis_changed(self, old, new):
        self._replace_underlay(old, new)

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

    def _replace_underlay(self, old, new):
        replace_in_list(self.underlays, old, new)

    def _replace_overlay(self, old, new):
        replace_in_list(self.overlays, old, new)