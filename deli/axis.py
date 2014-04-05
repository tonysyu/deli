""" Defines the PlotAxis class, and associated validator and UI.
"""
from numpy import array, around, dot, float64, sqrt

from enable.api import ColorTrait, LineStyle
from kiva.trait_defs.kiva_font_trait import KivaFont
from traits.api import Any, Float, Int, Str, Trait, Unicode, \
     Bool, Event, List, Array, Instance, Enum, Callable

from .ticks import AbstractTickGenerator, DefaultTickGenerator
from .abstract_mapper import AbstractMapper
from .abstract_overlay import AbstractOverlay
from .label import Label
from .utils import switch_trait_handler


def DEFAULT_TICK_FORMATTER(val):
    return ("%f"%val).rstrip("0").rstrip(".")


class PlotAxis(AbstractOverlay):

    # The mapper that drives this axis.
    mapper = Instance(AbstractMapper)

    # Keep an origin for plots that aren't attached to a component
    origin = Enum("bottom left", "top left", "bottom right", "top right")

    # The text of the axis title.
    title = Trait('', Str, Unicode) #May want to add PlotLabel option

    # The font of the title.
    title_font = KivaFont('modern 12')

    # The spacing between the axis line and the title
    title_spacing = Trait('auto', 'auto', Float)

    # The color of the title.
    title_color = ColorTrait("black")

    # The thickness (in pixels) of each tick.
    tick_weight = Float(1.0)

    # The color of the ticks.
    tick_color = ColorTrait("black")

    # The font of the tick labels.
    tick_label_font = KivaFont('modern 10')

    # The color of the tick labels.
    tick_label_color = ColorTrait("black")

    # The rotation of the tick labels.
    tick_label_rotate_angle = Float(0)

    # Whether to align to corners or edges (corner is better for 45 degree rotation)
    tick_label_alignment = Enum('edge', 'corner')

    # The margin around the tick labels.
    tick_label_margin = Int(2)

    # The distance of the tick label from the axis.
    tick_label_offset = Float(8.)

    # Whether the tick labels appear to the inside or the outside of the plot area
    tick_label_position = Enum("outside", "inside")

    # A callable that is passed the numerical value of each tick label and
    # that returns a string.
    tick_label_formatter = Callable(DEFAULT_TICK_FORMATTER)

    # The number of pixels by which the ticks extend into the plot area.
    tick_in = Int(5)

    # The number of pixels by which the ticks extend into the label area.
    tick_out = Int(5)

    # Are ticks visible at all?
    tick_visible = Bool(True)

    # The dataspace interval between ticks.
    tick_interval = Trait('auto', 'auto', Float)

    # A callable that implements the AbstractTickGenerator interface.
    tick_generator = Instance(AbstractTickGenerator)

    # The location of the axis relative to the plot.  This determines where
    # the axis title is located relative to the axis line.
    orientation = Enum("top", "bottom", "left", "right")

    # Is the axis line visible?
    axis_line_visible = Bool(True)

    # The color of the axis line.
    axis_line_color = ColorTrait("black")

    # The line thickness (in pixels) of the axis line.
    axis_line_weight = Float(1.0)

    # The dash style of the axis line.
    axis_line_style = LineStyle('solid')

    # A special version of the axis line that is more useful for geophysical
    # plots.
    small_haxis_style = Bool(False)

    # Does the axis ensure that its end labels fall within its bounding area?
    ensure_labels_bounded = Bool(False)

    # Does the axis prevent the ticks from being rendered outside its bounds?
    # This flag is off by default because the standard axis *does* render ticks
    # that encroach on the plot area.
    ensure_ticks_bounded = Bool(False)

    # Fired when the axis's range bounds change.
    updated = Event

    #------------------------------------------------------------------------
    # Override default values of inherited traits
    #------------------------------------------------------------------------

    # Background color (overrides AbstractOverlay). Axes usually let the color of
    # the container show through.
    bgcolor = ColorTrait("transparent")

    # Dimensions that the axis is resizable in (overrides PlotComponent).
    # Typically, axes are resizable in both dimensions.
    resizable = "hv"

    #------------------------------------------------------------------------
    # Private Traits
    #------------------------------------------------------------------------

    # Cached position calculations

    _tick_positions = Any #List
    _tick_label_list = Any
    _tick_label_positions = Any
    _tick_label_bounding_boxes = List
    _major_axis_size = Float
    _minor_axis_size = Float
    _major_axis = Array
    _title_orientation = Array
    _origin_point = Array
    _inside_vector = Array
    _axis_vector = Array
    _axis_pixel_vector = Array
    _end_axis_point = Array

    ticklabel_cache = List
    _cache_valid = Bool(False)

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def __init__(self, component=None, **kwargs):
        # TODO: change this back to a factory in the instance trait some day
        self.tick_generator = DefaultTickGenerator()
        # Override init so that our component gets set last.  We want the
        # _component_changed() event handler to get run last.
        super(PlotAxis, self).__init__(**kwargs)
        if component is not None:
            self.component = component

    #------------------------------------------------------------------------
    # PlotComponent and AbstractOverlay interface
    #------------------------------------------------------------------------

    def _do_layout(self, *args, **kw):
        """ Tells this component to do layout at a given size.

        Overrides Component.
        """
        self._layout_as_overlay(*args, **kw)

    def overlay(self, component, gc, view_bounds=None, mode='normal'):
        """ Draws this component overlaid on another component.

        Overrides AbstractOverlay.
        """
        self._draw_component(gc, view_bounds, mode, component)

    def _draw_component(self, gc, view_bounds=None, mode='normal', component=None):
        """ Draws the component.

        This method is preserved for backwards compatibility. Overrides
        PlotComponent.
        """
        if not self._cache_valid:
            self._calculate_geometry_overlay(component)
            self._compute_tick_positions(gc, component)
            self._compute_labels(gc)

        with gc:
            # slight optimization: if we set the font correctly on the
            # base gc before handing it in to our title and tick labels,
            # their set_font() won't have to do any work.
            gc.set_font(self.tick_label_font)

            if self.axis_line_visible:
                self._draw_axis_line(gc, self._origin_point, self._end_axis_point)

            self._draw_ticks(gc)
            self._draw_labels(gc)

        self._cache_valid = True

    #------------------------------------------------------------------------
    # Private draw routines
    #------------------------------------------------------------------------

    def _layout_as_overlay(self, size=None, force=False):
        """ Lays out the axis as an overlay on another component.
        """
        if self.component is not None:
            if self.orientation in ("left", "right"):
                self.y = self.component.y
                self.height = self.component.height
                self.width = self.component.padding_left
                self.x = self.component.outer_x
            else:
                self.x = self.component.x
                self.width = self.component.width
                self.height = self.component.padding_bottom
                self.y = self.component.outer_y

    def _draw_axis_line(self, gc, startpoint, endpoint):
        """ Draws the line for the axis.
        """
        with gc:
            gc.set_antialias(0)
            gc.set_line_width(self.axis_line_weight)
            gc.set_stroke_color(self.axis_line_color_)
            gc.set_line_dash(self.axis_line_style_)
            gc.move_to(*around(startpoint))
            gc.line_to(*around(endpoint))
            gc.stroke_path()

    def _draw_ticks(self, gc):
        """ Draws the tick marks for the axis.
        """
        gc.set_stroke_color(self.tick_color_)
        gc.set_line_width(self.tick_weight)
        gc.set_antialias(False)
        gc.begin_path()
        tick_in_vector = self._inside_vector*self.tick_in
        tick_out_vector = self._inside_vector*self.tick_out
        for tick_pos in self._tick_positions:
            gc.move_to(*(tick_pos + tick_in_vector))
            gc.line_to(*(tick_pos - tick_out_vector))
        gc.stroke_path()

    def _draw_labels(self, gc):
        """ Draws the tick labels for the axis.
        """
        # which axis are we moving away from the axis line along?
        axis_index = self._major_axis.argmin()

        inside_vector = self._inside_vector

        for i in range(len(self._tick_label_positions)):
            #We want a more sophisticated scheme than just 2 decimals all the time
            ticklabel = self.ticklabel_cache[i]
            tl_bounds = self._tick_label_bounding_boxes[i]

            base_position = self._tick_label_positions[i].copy()
            axis_dist = self.tick_label_offset + tl_bounds[axis_index]/2.0
            base_position -= inside_vector * axis_dist
            base_position -= tl_bounds/2.0

            tlpos = around(base_position)
            gc.translate_ctm(*tlpos)
            ticklabel.draw(gc)
            gc.translate_ctm(*(-tlpos))

    #------------------------------------------------------------------------
    # Private methods for computing positions and layout
    #------------------------------------------------------------------------

    def _compute_tick_positions(self, gc, overlay_component=None):
        """ Calculates the positions for the tick marks.
        """
        datalow = self.mapper.range.low
        datahigh = self.mapper.range.high
        screenhigh = self.mapper.high_pos
        screenlow = self.mapper.low_pos

        scale = 'linear'
        tick_list = array(self.tick_generator.get_ticks(datalow, datahigh,
                                                        datalow, datahigh,
                                                        self.tick_interval,
                                                        use_endpoints=False,
                                                        scale=scale), float64)

        mapped_tick_positions = (array(self.mapper.map_screen(tick_list))-screenlow) / \
                                            (screenhigh-screenlow)
        self._tick_positions = around(array([self._axis_vector*tickpos + self._origin_point \
                                for tickpos in mapped_tick_positions]))
        self._tick_label_list = tick_list
        self._tick_label_positions = self._tick_positions

    def _compute_labels(self, gc):
        """Generates the labels for tick marks.

        Waits for the cache to become invalid.
        """
        formatter = self.tick_label_formatter
        def build_label(val):
            tickstring = formatter(val) if formatter is not None else str(val)
            return Label(text=tickstring,
                         font=self.tick_label_font,
                         color=self.tick_label_color,
                         rotate_angle=self.tick_label_rotate_angle,
                         margin=self.tick_label_margin)

        self.ticklabel_cache = [build_label(val) for val in self._tick_label_list]
        self._tick_label_bounding_boxes = [array(ticklabel.get_bounding_box(gc), float)
                                               for ticklabel in self.ticklabel_cache]

    def _calculate_geometry_overlay(self, overlay_component=None):
        screenhigh = self.mapper.high_pos
        screenlow = self.mapper.low_pos

        if self.orientation in ('top', 'bottom'):
            self._major_axis_size = overlay_component.bounds[0]
            self._minor_axis_size = overlay_component.bounds[1]
            self._major_axis = array([1., 0.])
            self._title_orientation = array([0.,1.])
            self.title_angle = 0.0
            self._origin_point = array([overlay_component.x, overlay_component.y])
            self._inside_vector = array([0.0, 1.0])

        elif self.orientation in ('left', 'right'):
            self._major_axis_size = overlay_component.bounds[1]
            self._minor_axis_size = overlay_component.bounds[0]
            self._major_axis = array([0., 1.])
            self._title_orientation = array([-1., 0])
            self._origin_point = array([overlay_component.x, overlay_component.y])
            self._inside_vector = array([1.0, 0.0])
            self.title_angle = 90.0

        self._end_axis_point = abs(screenhigh-screenlow)*self._major_axis + self._origin_point
        self._axis_vector = self._end_axis_point - self._origin_point
        # This is the vector that represents one unit of data space in terms of screen space.
        self._axis_pixel_vector = self._axis_vector/sqrt(dot(self._axis_vector,self._axis_vector))

    #------------------------------------------------------------------------
    # Event handlers
    #------------------------------------------------------------------------

    def _bounds_items_changed(self, event):
        super(PlotAxis, self)._bounds_items_changed(event)
        self._layout_needed = True
        self._invalidate()

    def _mapper_changed(self, old, new):
        switch_trait_handler(old, new, 'updated', self.mapper_updated)
        self._invalidate()

    def mapper_updated(self):
        """
        Event handler that is bound to this axis's mapper's **updated** event
        """
        self._invalidate()

    def _position_items_changed(self, event):
        super(PlotAxis, self)._position_items_changed(event)
        self._cache_valid = False

    def _position_changed_for_component(self):
        self._cache_valid = False

    def _bounds_changed_for_component(self):
        self._cache_valid = False
        self._layout_needed = True

    def _invalidate(self):
        self._cache_valid = False
        self.invalidate_draw()
        if self.component:
            self.component.invalidate_draw()
