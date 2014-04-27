""" Defines the PlotAxis class, and associated validator and UI.
"""
from numpy import array, around

from enable.api import ColorTrait
from kiva.trait_defs.kiva_font_trait import KivaFont
from traits.api import Any, Float, Int, Event, Array, Instance, Callable

from .abstract_overlay import AbstractOverlay
from .artist.label_artist import LabelArtist
from .artist.line_artist import LineArtist
from .layout.grid_layout import BaseGridLayout, XGridLayout, YGridLayout


def DEFAULT_TICK_FORMATTER(val):
    return ("%f"%val).rstrip("0").rstrip(".")


class PlotAxis(AbstractOverlay):

    # The font of the tick labels.
    tick_label_font = KivaFont('modern 10')

    # The color of the tick labels.
    tick_label_color = ColorTrait("black")

    # The margin around the tick labels.
    tick_label_margin = Int(2)

    # The distance of the tick label from the axis.
    tick_label_offset = Float(8.)

    # A callable that is passed the numerical value of each tick label and
    # that returns a string.
    tick_label_formatter = Callable(DEFAULT_TICK_FORMATTER)

    #: Artist responsible for drawing tick labels.
    label_artist = Instance(LabelArtist)

    # The number of pixels by which the ticks extend into the plot area.
    tick_in = Int(5)

    # The number of pixels by which the ticks extend into the label area.
    tick_out = Int(5)

    # A tick grid that controls tick positioning
    tick_grid = Instance(BaseGridLayout)

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
    _major_axis = Array
    _xy_origin = Array
    _inside_vector = Array
    _axis_vector = Array
    _end_axis_point = Array
    _tick_starts = Array
    _tick_ends = Array

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
        self.line_artist.draw_segments(gc, self._xy_origin,
                                           self._end_axis_point)

    def _draw_ticks(self, gc):
        """ Draws the tick marks for the axis.
        """
        self.tick_artist.update_context(gc)
        self.tick_artist.draw_segments(gc, self._tick_starts, self._tick_ends)

    def _draw_labels(self, gc):
        """ Draws the tick labels for the axis.
        """
        inside_vector = self._inside_vector

        axial_offsets = self.tick_grid.axial_offsets
        for screen_point, data_offset in zip(self._xy_tick, axial_offsets):
            text = str(data_offset)

            xy_screen = screen_point
            axis_dist = self.tick_label_offset
            xy_screen -= inside_vector * axis_dist

            tlpos = around(xy_screen)
            gc.translate_ctm(*tlpos)
            self.label_artist.draw(gc, text)
            gc.translate_ctm(*(-tlpos))

    #------------------------------------------------------------------------
    # Private methods for computing positions and layout
    #------------------------------------------------------------------------

    def _compute_tick_positions(self):
        """ Calculates the positions for the tick marks.
        """
        x_norm = self.tick_grid.norm_axial_offsets[:, None]
        self._xy_tick = self._axis_vector * x_norm + self._xy_origin
        self._tick_starts, self._tick_ends = self._get_tick_segments()

    def _calculate_geometry_overlay(self, component=None):
        screen_size = self.screen_size(component)

        self._set_geometry_traits(component)

        self._end_axis_point = screen_size*self._major_axis + self._xy_origin
        self._axis_vector = self._end_axis_point - self._xy_origin

    def _set_geometry_traits(self, component):
        raise NotImplementedError()

    #------------------------------------------------------------------------
    # Event handlers
    #------------------------------------------------------------------------

    def _bounds_changed_for_component(self):
        self._layout_needed = True

    def _invalidate(self):
        self.invalidate_draw()
        if self.component:
            self.component.invalidate_draw()


class XAxis(PlotAxis):

    def _label_artist_default(self):
        return LabelArtist(font=self.tick_label_font,
                           y_origin='top',
                           color=self.tick_label_color,
                           margin=self.tick_label_margin)

    def _tick_grid_default(self):
        return XGridLayout(data_bbox=self.component.data_bbox)

    def _set_geometry_traits(self, component):
        self._major_axis = array([1., 0.])
        self._xy_origin = array([component.x, component.y])
        self._inside_vector = array([0.0, 1.0])

    def _get_tick_segments(self):
        starts = self._xy_tick + [0, self.tick_in]
        ends = self._xy_tick - [0, self.tick_out]
        return starts, ends

    def screen_size(self, component):
        return component.screen_bbox.width


class YAxis(PlotAxis):

    def _label_artist_default(self):
        return LabelArtist(font=self.tick_label_font,
                           x_origin='right',
                           color=self.tick_label_color,
                           margin=self.tick_label_margin)

    def _tick_grid_default(self):
        return YGridLayout(data_bbox=self.component.data_bbox)

    def _set_geometry_traits(self, component):
        self._major_axis = array([0., 1.])
        self._xy_origin = array([component.x, component.y])
        self._inside_vector = array([1.0, 0.0])

    def _get_tick_segments(self):
        starts = self._xy_tick + [self.tick_in, 0]
        ends = self._xy_tick - [self.tick_out, 0]
        return starts, ends

    def screen_size(self, component):
        return component.screen_bbox.height
