""" Defines the DataView class, and associated property traits and property
functions.
"""
from traits.api import Bool, Enum, Instance, Property

from .abstract_overlay import AbstractOverlay
from .axis import XAxis, YAxis
from .base_1d_mapper import Base1DMapper
from .data_range_2d import DataRange2D
from .grid import PlotGrid
from .linear_mapper import LinearMapper
from .plot_containers import OverlayPlotContainer


class DataView(OverlayPlotContainer):
    """ Represents a mapping from 2-D data space into 2-D screen space.

    It can house renderers and other plot components, and otherwise behaves
    just like a normal PlotContainer.
    """

    # The default location of the origin for new plots
    origin = Enum('bottom left', 'top left', 'bottom right', 'top right')

    # The mapper to use for the x data.
    x_mapper = Instance(Base1DMapper)

    # The mapper to use for y data.
    y_mapper = Instance(Base1DMapper)

    # The range used for the x data.
    x_range = Property

    # The range used for the y data.
    y_range = Property

    # The 2-D data range whose x- and y-ranges are exposed as the
    # **x_range** and **y_range** property traits. This allows
    # supporting both XY plots and 2-D (image) plots.
    range2d = Instance(DataRange2D)

    #------------------------------------------------------------------------
    # Axis and Grids
    #------------------------------------------------------------------------

    # The horizontal axis.
    x_axis = Instance(AbstractOverlay)

    # The vertical axis.
    y_axis = Instance(AbstractOverlay)

    # The grid that intersects the x-axis, i.e., a set of vertical lines.
    x_grid = Instance(PlotGrid)

    # The grid that intersects the y-axis, i.e., a set of horizontal lines.
    y_grid = Instance(PlotGrid)

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

    border_visible = True

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
        if not self.x_mapper:
            imap = LinearMapper(range=self.range2d.x_range)
            self.x_mapper = imap

        if not self.y_mapper:
            vmap = LinearMapper(range=self.range2d.y_range)
            self.y_mapper = vmap

        if not self.x_grid and self.auto_grid:
            self.x_grid = PlotGrid(mapper=self.x_mapper, orientation="vertical",
                                   component=self)
        if not self.y_grid and self.auto_grid:
            self.y_grid = PlotGrid(mapper=self.y_mapper, orientation="horizontal",
                                   component=self)

        if not self.x_axis and self.auto_axis:
            self.x_axis = XAxis(mapper=self.x_mapper, component=self)

        if not self.y_axis and self.auto_axis:
            self.y_axis = YAxis(mapper=self.y_mapper, component=self)

    #-------------------------------------------------------------------------
    # Event handlers
    #-------------------------------------------------------------------------

    def _update_mappers(self):
        if self.x_mapper is not None:
            self.x_mapper.low_pos = self.x
            self.x_mapper.high_pos = self.x2

        if self.y_mapper is not None:
            self.y_mapper.low_pos = self.y
            self.y_mapper.high_pos = self.y2

        self.invalidate_draw()

    def _bounds_changed(self, old, new):
        super(DataView, self)._bounds_changed(old, new)
        self._update_mappers()

    def _position_changed(self, old, new):
        super(DataView, self)._position_changed(old, new)
        self._update_mappers()

    def _x_mapper_changed(self, old, new):
        new.range = self.x_range

    def _y_mapper_changed(self, old, new):
        new.range = self.y_range

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

    def _range2d_default(self):
        return DataRange2D()

    #------------------------------------------------------------------------
    # Property getters and setters
    #------------------------------------------------------------------------

    def _get_x_range(self):
        return self.range2d.x_range

    def _get_y_range(self):
        return self.range2d.y_range
