""" Defines the PlotGrid class, and associated Traits UI View and validator
function.
"""
from numpy import around, array, column_stack, float64, zeros, zeros_like

from enable.api import black_color_trait, LineStyle
from traits.api import (Any, Bool, Enum, Float, Instance, CInt, Trait,
                        Property, on_trait_change)

from .abstract_overlay import AbstractOverlay
from .abstract_mapper import AbstractMapper
from .ticks import AbstractTickGenerator, DefaultTickGenerator
from .utils import switch_trait_handler


def Alias(name):
    return Property(lambda obj: getattr(obj, name),
                    lambda obj, val: setattr(obj, name, val))


class PlotGrid(AbstractOverlay):
    """ An overlay that represents a grid.

    A grid is a set of parallel lines, horizontal or vertical. You can use
    multiple grids with different settings for the horizontal and vertical
    lines in a plot.
    """

    #------------------------------------------------------------------------
    # Data-related traits
    #------------------------------------------------------------------------

    # The mapper (and associated range) that drive this PlotGrid.
    mapper = Instance(AbstractMapper)

    # The dataspace interval between grid lines.
    grid_interval = Trait('auto', 'auto', Float)

    # The dataspace value at which to start this grid.  If None, then
    # uses the mapper.range.low.
    data_min = Trait(None, None, Float)

    # The dataspace value at which to end this grid.  If None, then uses
    # the mapper.range.high.
    data_max = Trait(None, None, Float)

    # A callable that implements the AbstractTickGenerator Interface.
    tick_generator = Instance(AbstractTickGenerator)

    #------------------------------------------------------------------------
    # Layout traits
    #------------------------------------------------------------------------

    # The orientation of the grid lines.  "horizontal" means that the grid
    # lines are parallel to the X axis and the ticker and grid interval
    # refer to the Y axis.
    orientation = Enum('horizontal', 'vertical')

    # Draw the ticks starting at the end of the mapper range? If False, the
    # ticks are drawn starting at 0. This setting can be useful to keep the
    # grid from from "flashing" as the user resizes the plot area.
    flip_axis = Bool(False)

    # Dimensions that the grid is resizable in (overrides PlotComponent).
    resizable = "hv"

    #------------------------------------------------------------------------
    # Appearance traits
    #------------------------------------------------------------------------

    # The color of the grid lines.
    line_color = black_color_trait

    # The style (i.e., dash pattern) of the grid lines.
    line_style = LineStyle('solid')

    # The thickness, in pixels, of the grid lines.
    line_width = CInt(1)
    line_weight = Alias("line_width")

    #------------------------------------------------------------------------
    # Private traits; mostly cached information
    #------------------------------------------------------------------------

    _cache_valid = Bool(False)
    _tick_list = Any
    _tick_positions = Any

    # An array (N,2) of start,end positions in the transverse direction
    # i.e. the direction corresponding to self.orientation
    _tick_extents = Any

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def __init__(self, **traits):
        # TODO: change this back to a factory in the instance trait some day
        self.tick_generator = DefaultTickGenerator()
        super(PlotGrid, self).__init__(**traits)
        self.bgcolor = "none" #make sure we're transparent

    @on_trait_change("bounds,bounds_items,position,position_items")
    def invalidate(self):
        """ Invalidate cached information about the grid.
        """
        self._reset_cache()

    #------------------------------------------------------------------------
    # PlotComponent and AbstractOverlay interface
    #------------------------------------------------------------------------

    def do_layout(self, *args, **kw):
        """ Tells this component to do layout at a given size.

        Overrides PlotComponent.
        """
        self._layout_as_overlay(*args, **kw)

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _layout_as_overlay(self, size=None, force=False):
        """ Lays out the axis as an overlay on another component.
        """
        if self.component is not None:
            self.position = self.component.position
            self.bounds = self.component.bounds

    def _reset_cache(self):
        """ Clears the cached tick positions.
        """
        self._tick_positions = array([], dtype=float)
        self._tick_extents = array([], dtype=float)
        self._cache_valid = False

    def _compute_ticks(self, component=None):
        """ Calculates the positions for the grid lines.
        """
        datalow = self.mapper.range.low
        datahigh = self.mapper.range.high

        if component is not None:
            bounds = component.bounds
            position = component.position

        ticks = self.tick_generator.get_ticks(
            datalow, datahigh, datalow, datahigh, self.grid_interval,
            use_endpoints=False, scale='linear'
        )
        tick_positions = self.mapper.map_screen(array(ticks, float64))

        if self.orientation == 'horizontal':
            start = zeros_like(tick_positions) + position[0]
            self._tick_positions = around(column_stack((start, tick_positions)))
        elif self.orientation == 'vertical':
            end = zeros_like(tick_positions) + position[1]
            self._tick_positions = around(column_stack((tick_positions, end)))

        # Compute the transverse direction extents
        self._tick_extents = zeros((len(ticks), 2), dtype=float)

        if self.orientation == 'horizontal':
            extents = (position[0], position[0] + bounds[0])
        elif self.orientation == 'vertical':
            extents = (position[1], position[1] + bounds[1])
        self._tick_extents[:] = extents

        self._cache_valid = True

    def overlay(self, other_component, gc, view_bounds=None, mode="normal"):
        """ Draws this component overlaid on another component.

        Overrides AbstractOverlay.
        """
        self._compute_ticks(other_component)
        self._draw_component(gc, view_bounds, mode)
        self._cache_valid = False

    def _draw_component(self, gc, view_bounds=None, mode="normal"):
        """ Draws the component.

        This method is preserved for backwards compatibility. Overrides
        PlotComponent.
        """
        # What we're really trying to do with a grid is plot contour lines in
        # the space of the plot.  In a rectangular plot, these will always be
        # straight lines.
        with gc:
            gc.set_line_width(self.line_weight)
            gc.set_line_dash(self.line_style_)
            gc.set_stroke_color(self.line_color_)
            gc.set_antialias(False)

            gc.clip_to_rect(*(self.component.position + self.component.bounds))

            gc.begin_path()
            if self.orientation == "horizontal":
                starts = self._tick_positions.copy()
                starts[:,0] = self._tick_extents[:,0]
                ends = self._tick_positions.copy()
                ends[:,0] = self._tick_extents[:,1]
            else:
                starts = self._tick_positions.copy()
                starts[:,1] = self._tick_extents[:,0]
                ends = self._tick_positions.copy()
                ends[:,1] = self._tick_extents[:,1]
            gc.line_set(starts, ends)
            gc.stroke_path()

    def _mapper_changed(self, old, new):
        switch_trait_handler(old, new, 'updated', self.mapper_updated)
        self.invalidate()

    def mapper_updated(self):
        """
        Event handler that is bound to this mapper's **updated** event.
        """
        self.invalidate()

    def _position_changed_for_component(self):
        self.invalidate()

    def _bounds_changed_for_component(self):
        self.invalidate()

    #------------------------------------------------------------------------
    # Event handlers for visual attributes.  These mostly just call request_redraw()
    #------------------------------------------------------------------------

    @on_trait_change("visible,line_color,line_style,line_weight")
    def visual_attr_changed(self):
        """ Called when an attribute that affects the appearance of the grid
        is changed.
        """
        self.component.invalidate_draw()
        self.component.request_redraw()

    def _orientation_changed(self):
        self.invalidate()
        self.visual_attr_changed()
