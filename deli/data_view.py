""" Defines the DataView class, and associated property traits and property
functions.
"""
from traits.api import Bool, Enum, Instance, Property

from .abstract_overlay import AbstractOverlay
from .axis import PlotAxis
from .base_1d_mapper import Base1DMapper
from .data_range_2d import DataRange2D
from .grid import PlotGrid
from .linear_mapper import LinearMapper
from .plot_containers import OverlayPlotContainer


def get_mapper(self, attr_name):
    """ Getter function used by OrientedMapperProperty.
    """
    if attr_name in "x_mapper":
        return self.index_mapper
    else:
        return self.value_mapper

def set_mapper(self, attr_name, new):
    """ Setter function used by OrientedMapperProperty.
    """
    if attr_name == "x_mapper":
        self.index_mapper = new
    else:
        self.value_mapper = new

# Property that represents a mapper for an orientation.
OrientedMapperProperty = Property(get_mapper, set_mapper)


def get_axis(self, attr_name):
    """ Getter function used by AxisProperty.
    """
    if attr_name == "index_axis":
        return self.x_axis
    else:
        return self.y_axis

def set_axis(self, attr_name, new):
    """ Setter function used by AxisProperty.
    """
    if attr_name == "index_axis":
        self.x_axis = new
    else:
        self.y_axis = new

# Property that represents an axis.
AxisProperty = Property(get_axis, set_axis)


def get_grid(self, attr_name):
    """ Getter function used by GridProperty.
    """
    if attr_name == "index_grid":
        return self.y_grid
    else:
        return self.x_grid

def set_grid(self, attr_name, new):
    """ Setter function used by GridProperty.
    """
    if attr_name == "value_grid":
        self.y_grid = new
    else:
        self.y_grid = new

# Property that represents a grid for a particular orientation.
GridProperty = Property(get_grid, set_grid)


class DataView(OverlayPlotContainer):
    """ Represents a mapping from 2-D data space into 2-D screen space.

    It can house renderers and other plot components, and otherwise behaves
    just like a normal PlotContainer.
    """

    # The default location of the origin  for new plots
    default_origin = Enum("bottom left", "top left",
                          "bottom right", "top right")

    # The origin reported to axes, etc
    origin = Property(depends_on='default_origin')

    # Whether our map_screen and map_data should treat screen-space
    # coords as being in our coordinate space or in our contained
    # coordinate space.

    # The mapper to use for the index data.
    index_mapper = Instance(Base1DMapper)

    # The mapper to use for value data.
    value_mapper = Instance(Base1DMapper)

    # For x-y plots, the scale of the index axis.
    index_scale = Enum("linear", "log")

    # For x-y plots, the scale of the index axis.
    value_scale = Enum("linear", "log")

    # The range used for the index data.
    index_range = Property

    # The range used for the value data.
    value_range = Property

    # The 2-D data range whose x- and y-ranges are exposed as the
    # **index_range** and **value_range** property traits. This allows
    # supporting both XY plots and 2-D (image) plots.
    range2d = Instance(DataRange2D)

    # Convenience property that offers access to whatever mapper corresponds
    # to the X-axis.
    x_mapper = OrientedMapperProperty

    # Convenience property that offers access to whatever mapper corresponds
    # to the Y-axis
    y_mapper = OrientedMapperProperty

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

    # Convenience property for accessing the index axis, which can be X or Y,
    # depending on **orientation**.
    index_axis = AxisProperty
    # Convenience property for accessing the value axis, which can be Y or X,
    # depending on **orientation**.
    value_axis = AxisProperty
    # Convenience property for accessing the index grid, which can be horizontal
    # or vertical, depending on **orientation**.
    index_grid = GridProperty
    # Convenience property for accessing the value grid, which can be vertical
    # or horizontal, depending on **orientation**.
    value_grid = GridProperty

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
        if not self.index_mapper:
            imap = LinearMapper(range=self.range2d.x_range)
            self.index_mapper = imap

        if not self.value_mapper:
            vmap = LinearMapper(range=self.range2d.y_range)
            self.value_mapper = vmap

        grid_color = 'lightgray'

        if not self.x_grid and self.auto_grid:
            self.x_grid = PlotGrid(mapper=self.x_mapper, orientation="vertical",
                                  line_color=grid_color, line_style="dot",
                                  component=self)
        if not self.y_grid and self.auto_grid:
            self.y_grid = PlotGrid(mapper=self.y_mapper, orientation="horizontal",
                                  line_color=grid_color, line_style="dot",
                                  component=self)

        if not self.x_axis and self.auto_axis:
            self.x_axis = PlotAxis(mapper=self.x_mapper, orientation="bottom",
                                  component=self)

        if not self.y_axis and self.auto_axis:
            self.y_axis = PlotAxis(mapper=self.y_mapper, orientation="left",
                                  component=self)

    #-------------------------------------------------------------------------
    # Event handlers
    #-------------------------------------------------------------------------

    def _update_mappers(self):

        x = self.x
        x2 = self.x2
        y = self.y
        y2 = self.y2

        if self.x_mapper is not None:
            self.x_mapper.low_pos = x
            self.x_mapper.high_pos = x2

        if self.y_mapper is not None:
            self.y_mapper.low_pos = y
            self.y_mapper.high_pos = y2

        self.invalidate_draw()

    def _bounds_changed(self, old, new):
        super(DataView, self)._bounds_changed(old, new)
        self._update_mappers()

    def _position_changed(self, old, new):
        super(DataView, self)._position_changed(old, new)
        self._update_mappers()

    def _index_mapper_changed(self, old, new):
        new.range = self.index_range

    def _value_mapper_changed(self, old, new):
        new.range = self.value_range

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

    def _get_index_range(self):
        return self.range2d.x_range

    def _get_value_range(self):
        return self.range2d.y_range

    def _get_origin(self):
        return self.default_origin
