""" Defines the XAxis and YAxis classes.
"""
from numpy import array

from enable.api import ColorTrait
from kiva.trait_defs.kiva_font_trait import KivaFont
from traits.api import Array, Callable, Event, Float, Instance, Int

from .abstract_overlay import AbstractOverlay
from .artist.label_artist import LabelArtist
from .artist.line_artist import LineArtist
from .layout.grid_layout import BaseGridLayout, XGridLayout, YGridLayout


DEFAULT_COLOR = 'dimgray'


def DEFAULT_TICK_FORMATTER(val):
    return ("%f"%val).rstrip("0").rstrip(".")


class BaseAxis(AbstractOverlay):

    # The font of the tick labels.
    tick_label_font = KivaFont('modern 10')

    # The color of the tick labels.
    tick_label_color = ColorTrait(DEFAULT_COLOR)

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

    tick_artist = Instance(LineArtist, (), {'color': DEFAULT_COLOR})

    line_artist = Instance(LineArtist, (), {'color': DEFAULT_COLOR})

    #------------------------------------------------------------------------
    # Private Traits
    #------------------------------------------------------------------------

    # Cached position calculations
    _xy_tick = Array

    #------------------------------------------------------------------------
    # Public interface
    #------------------------------------------------------------------------

    def __init__(self, component=None, **kwargs):
        # Override init so that our component gets set last.  We want the
        # _component_changed() event handler to get run last.
        super(BaseAxis, self).__init__(**kwargs)
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
        xy_axis_limits = self._compute_xy_end_points(component)
        tick_starts, tick_ends = self._compute_tick_positions(*xy_axis_limits)

        with gc:
            gc.set_antialias(False)
            gc.set_font(self.tick_label_font)

            self._draw_axis_line(gc, *xy_axis_limits)
            self._draw_ticks(gc, tick_starts, tick_ends)
            self._draw_labels(gc)

    #------------------------------------------------------------------------
    # Private draw routines
    #------------------------------------------------------------------------

    def _draw_axis_line(self, gc, xy_axis_min, xy_axis_max):
        """ Draws the line for the axis. """
        self.line_artist.update_context(gc)
        self.line_artist.draw_segments(gc, xy_axis_min, xy_axis_max)

    def _draw_ticks(self, gc, tick_starts, tick_ends):
        """ Draws the tick marks for the axis.
        """
        self.tick_artist.update_context(gc)
        self.tick_artist.draw_segments(gc, tick_starts, tick_ends)

    def _draw_labels(self, gc):
        """ Draws the tick labels for the axis.
        """
        axial_offsets = self.tick_grid.axial_offsets
        for xy_screen, data_offset in zip(self._xy_tick, axial_offsets):
            tick_label = str(data_offset)
            gc.translate_ctm(*xy_screen)
            self.label_artist.draw(gc, tick_label)
            gc.translate_ctm(*(-xy_screen))

    #------------------------------------------------------------------------
    # Private methods for computing positions and layout
    #------------------------------------------------------------------------

    def _compute_tick_positions(self, xy_axis_min, xy_axis_max):
        """ Calculates the positions for the tick marks.
        """
        x_norm = self.tick_grid.axial_offsets_norm[:, None]
        axis_vector = xy_axis_max - xy_axis_min
        self._xy_tick = axis_vector * x_norm + xy_axis_min
        return self._get_tick_segments()

    def _compute_xy_end_points(self, component=None):
        end_xy_offset = self._get_end_xy_offset(component)

        xy_axis_min = array([self.component.x, self.component.y])
        xy_axis_max = end_xy_offset + xy_axis_min
        return xy_axis_min, xy_axis_max

    #------------------------------------------------------------------------
    # Event handlers
    #------------------------------------------------------------------------

    def _bounds_changed_for_component(self):
        self._layout_needed = True

    def _invalidate(self):
        self.invalidate_draw()
        if self.component:
            self.component.invalidate_draw()


class XAxis(BaseAxis):

    def _label_artist_default(self):
        return LabelArtist(font=self.tick_label_font,
                           y_origin='top',
                           y_offset=-self.tick_label_offset,
                           color=self.tick_label_color,
                           margin=self.tick_label_margin)

    def _tick_grid_default(self):
        return XGridLayout(data_bbox=self.component.data_bbox)

    def _get_tick_segments(self):
        starts = self._xy_tick + [0, self.tick_in]
        ends = self._xy_tick - [0, self.tick_out]
        return starts, ends

    def _get_end_xy_offset(self, component):
        return array([component.screen_bbox.width, 0])


class YAxis(BaseAxis):

    def _label_artist_default(self):
        return LabelArtist(font=self.tick_label_font,
                           x_origin='right',
                           x_offset=-self.tick_label_offset,
                           color=self.tick_label_color,
                           margin=self.tick_label_margin)

    def _tick_grid_default(self):
        return YGridLayout(data_bbox=self.component.data_bbox)

    def _get_tick_segments(self):
        starts = self._xy_tick + [self.tick_in, 0]
        ends = self._xy_tick - [self.tick_out, 0]
        return starts, ends

    def _get_end_xy_offset(self, component):
        return array([0, component.screen_bbox.height])
