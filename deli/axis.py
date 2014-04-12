""" Defines the PlotAxis class, and associated validator and UI.
"""
from numpy import array, around

from enable.api import ColorTrait
from kiva.trait_defs.kiva_font_trait import KivaFont
from traits.api import Any, Float, Int, Event, List, Array, Instance, Callable

from .abstract_mapper import AbstractMapper
from .abstract_overlay import AbstractOverlay
from .label import Label
from .line_artist import LineArtist
from .ticks import TickGrid
from .utils import switch_trait_handler


def DEFAULT_TICK_FORMATTER(val):
    return ("%f"%val).rstrip("0").rstrip(".")


class PlotAxis(AbstractOverlay):

    # The mapper that drives this axis.
    mapper = Instance(AbstractMapper)

    # The font of the tick labels.
    tick_label_font = KivaFont('modern 10')

    # The color of the tick labels.
    tick_label_color = ColorTrait("black")

    # The rotation of the tick labels.
    tick_label_rotate_angle = Float(0)

    # The margin around the tick labels.
    tick_label_margin = Int(2)

    # The distance of the tick label from the axis.
    tick_label_offset = Float(8.)

    # A callable that is passed the numerical value of each tick label and
    # that returns a string.
    tick_label_formatter = Callable(DEFAULT_TICK_FORMATTER)

    # The number of pixels by which the ticks extend into the plot area.
    tick_in = Int(5)

    # The number of pixels by which the ticks extend into the label area.
    tick_out = Int(5)

    # A tick grid that controls tick positioning
    tick_grid = Instance(TickGrid, ())

    # Fired when the axis's range bounds change.
    updated = Event

    #------------------------------------------------------------------------
    # Appearance traits
    #------------------------------------------------------------------------

    tick_artist = Instance(LineArtist, ())

    line_artist = Instance(LineArtist, ())

    #------------------------------------------------------------------------
    # Private Traits
    #------------------------------------------------------------------------

    # Cached position calculations

    _xy_tick = Any #List
    _tick_label_bbox = List
    _major_axis = Array
    _xy_origin = Array
    _inside_vector = Array
    _axis_vector = Array
    _end_axis_point = Array

    _tick_label_cache = List

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def __init__(self, component=None, **kwargs):
        # Override init so that our component gets set last.  We want the
        # _component_changed() event handler to get run last.
        super(PlotAxis, self).__init__(**kwargs)
        if component is not None:
            self.component = component

    #------------------------------------------------------------------------
    # PlotComponent and AbstractOverlay interface
    #------------------------------------------------------------------------

    def overlay(self, component, gc, view_bounds=None, mode='normal'):
        """ Draws this component overlaid on another component.

        Overrides AbstractOverlay.
        """
        self._draw_component(gc, view_bounds, component)

    def _draw_component(self, gc, view_bounds=None, component=None):
        """ Draws the component.

        This method is preserved for backwards compatibility. Overrides
        PlotComponent.
        """
        self._calculate_geometry_overlay(component)
        self._compute_tick_positions()
        self._compute_labels(gc)

        with gc:
            gc.set_antialias(False)
            gc.set_font(self.tick_label_font)

            self._draw_axis_line(gc)
            self._draw_ticks(gc)
            self._draw_labels(gc)

    #------------------------------------------------------------------------
    # Private draw routines
    #------------------------------------------------------------------------

    def _draw_axis_line(self, gc):
        """ Draws the line for the axis. """
        self.line_artist.update_context(gc)

        gc.move_to(*around(self._xy_origin))
        gc.line_to(*around(self._end_axis_point))
        gc.stroke_path()

    def _draw_ticks(self, gc):
        """ Draws the tick marks for the axis.
        """
        self.tick_artist.update_context(gc)

        gc.begin_path()
        gc.line_set(self._tick_starts, self._tick_ends)
        gc.stroke_path()

    def _draw_labels(self, gc):
        """ Draws the tick labels for the axis.
        """
        offset_index = self._major_axis.argmin()

        inside_vector = self._inside_vector

        for i in range(len(self._xy_tick)):
            tick_label = self._tick_label_cache[i]
            bbox = self._tick_label_bbox[i]

            base_position = self._xy_tick[i].copy()
            axis_dist = self.tick_label_offset + bbox[offset_index]/2.0
            base_position -= inside_vector * axis_dist
            base_position -= bbox/2.0

            tlpos = around(base_position)
            gc.translate_ctm(*tlpos)
            tick_label.draw(gc)
            gc.translate_ctm(*(-tlpos))

    #------------------------------------------------------------------------
    # Private methods for computing positions and layout
    #------------------------------------------------------------------------

    def _compute_tick_positions(self):
        """ Calculates the positions for the tick marks.
        """
        self.tick_grid.update(self.mapper)
        x_norm = self.tick_grid.x_norm[:, None]
        self._xy_tick = self._axis_vector * x_norm + self._xy_origin
        self._tick_starts, self._tick_ends = self._get_tick_segments()

    def _compute_labels(self, gc):
        """Generates the labels for tick marks.
        """
        formatter = self.tick_label_formatter
        def build_label(val):
            label = formatter(val) if formatter is not None else str(val)
            return Label(text=label,
                         font=self.tick_label_font,
                         color=self.tick_label_color,
                         rotate_angle=self.tick_label_rotate_angle,
                         margin=self.tick_label_margin)

        self._tick_label_cache = [build_label(val)
                                  for val in self.tick_grid.x_data]
        self._tick_label_bbox = [array(tick_label.get_bbox(gc), float)
                                 for tick_label in self._tick_label_cache]

    def _calculate_geometry_overlay(self, component=None):
        screen_size = self.mapper.high_pos - self.mapper.low_pos

        self._set_geometry_traits(component)

        self._end_axis_point = screen_size*self._major_axis + self._xy_origin
        self._axis_vector = self._end_axis_point - self._xy_origin

    def _set_geometry_traits(self, component):
        raise NotImplementedError()

    #------------------------------------------------------------------------
    # Event handlers
    #------------------------------------------------------------------------

    def _mapper_changed(self, old, new):
        switch_trait_handler(old, new, 'updated', self.mapper_updated)
        self._invalidate()

    def mapper_updated(self):
        """
        Event handler that is bound to this axis's mapper's **updated** event
        """
        self._invalidate()

    def _bounds_changed_for_component(self):
        self._layout_needed = True

    def _invalidate(self):
        self.invalidate_draw()
        if self.component:
            self.component.invalidate_draw()


class XAxis(PlotAxis):

    def _set_geometry_traits(self, component):
        self._major_axis = array([1., 0.])
        self._xy_origin = array([component.x, component.y])
        self._inside_vector = array([0.0, 1.0])

    def _get_tick_segments(self):
        starts = self._xy_tick + [0, self.tick_in]
        ends = self._xy_tick - [0, self.tick_out]
        return starts, ends


class YAxis(PlotAxis):

    def _set_geometry_traits(self, component):
        self._major_axis = array([0., 1.])
        self._xy_origin = array([component.x, component.y])
        self._inside_vector = array([1.0, 0.0])

    def _get_tick_segments(self):
        starts = self._xy_tick + [self.tick_in, 0]
        ends = self._xy_tick - [self.tick_out, 0]
        return starts, ends
