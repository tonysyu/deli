""" Defines the XAxis and YAxis classes.
"""
import numpy as np

from traits.api import Array, Instance

from .abstract_overlay import AbstractOverlay
from .artist.label_artist import LabelArtist
from .artist.tick_artist import XTickArtist, YTickArtist
from .artist.tick_label_artist import XTickLabelArtist, YTickLabelArtist
from .artist.line_artist import LineArtist
from .layout.bbox_transform import BboxTransform
from .layout.grid_layout import BaseGridLayout, XGridLayout, YGridLayout


DEFAULT_COLOR = 'dimgray'
DEFAULT_OFFSET = 8.0


class BaseAxis(AbstractOverlay):

    # A tick grid that controls tick positioning
    tick_grid = Instance(BaseGridLayout)

    #: Transform from data-space to screen-space.
    data_to_screen = Instance(BboxTransform)

    #------------------------------------------------------------------------
    # Appearance traits
    #------------------------------------------------------------------------

    #: Artist responsible for drawing tick labels.
    tick_label_artist = Instance(LabelArtist)

    #: Artist responsible for drawing ticks.
    tick_artist = Instance(LineArtist)

    #: Artist responsible for drawing the axis line.
    line_artist = Instance(LineArtist, {'color': DEFAULT_COLOR})

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
        self._update_tick_positions(*xy_axis_limits)

        with gc:
            self._draw_axis_line(gc, *xy_axis_limits)
            self._draw_ticks(gc)
            self._draw_labels(gc)

    #------------------------------------------------------------------------
    # Private draw routines
    #------------------------------------------------------------------------

    def _draw_axis_line(self, gc, xy_axis_min, xy_axis_max):
        """ Draws the line for the axis. """
        self.line_artist.update_context(gc)
        self.line_artist.draw_segments(gc, xy_axis_min, xy_axis_max)

    def _draw_ticks(self, gc):
        """ Draws the tick marks for the axis.
        """
        self.tick_artist.update_context(gc)
        self.tick_artist.draw(gc, self.tick_grid.axial_offsets)

    def _draw_labels(self, gc):
        """ Draws the tick labels for the axis.
        """
        axial_offsets = self.tick_grid.axial_offsets
        for xy_screen, data_offset in zip(self._xy_tick, axial_offsets):
            tick_label = str(data_offset)
            gc.translate_ctm(*xy_screen)
            self.tick_label_artist.draw(gc, tick_label)
            gc.translate_ctm(*(-xy_screen))

    #------------------------------------------------------------------------
    # Private methods for computing positions and layout
    #------------------------------------------------------------------------

    def _update_tick_positions(self, xy_axis_min, xy_axis_max):
        """ Calculates the positions for the tick marks.
        """
        x_norm = self.tick_grid.axial_offsets_norm[:, None]
        axis_vector = xy_axis_max - xy_axis_min
        self._xy_tick = axis_vector * x_norm + xy_axis_min

    def _compute_xy_end_points(self, component=None):
        end_xy_offset = self._get_end_xy_offset(component)

        xy_axis_min = np.array([self.component.x, self.component.y])
        xy_axis_max = end_xy_offset + xy_axis_min
        return xy_axis_min, xy_axis_max

    def _data_to_screen_default(self):
        component = self.component
        return BboxTransform(component.data_bbox, component.screen_bbox)


class XAxis(BaseAxis):

    def _tick_artist_default(self):
        return XTickArtist(color=DEFAULT_COLOR,
                           position=self.component.y,
                           offset_transform=self.data_to_screen)

    def _tick_label_artist_default(self):
        return XTickLabelArtist(offset=-DEFAULT_OFFSET, color=DEFAULT_COLOR)

    def _tick_grid_default(self):
        return XGridLayout(data_bbox=self.component.data_bbox)

    def _get_end_xy_offset(self, component):
        return np.array([component.screen_bbox.width, 0])


class YAxis(BaseAxis):

    def _tick_artist_default(self):
        return YTickArtist(color=DEFAULT_COLOR,
                           position=self.component.x,
                           offset_transform=self.data_to_screen)

    def _tick_label_artist_default(self):
        return YTickLabelArtist(offset=-DEFAULT_OFFSET, color=DEFAULT_COLOR)

    def _tick_grid_default(self):
        return YGridLayout(data_bbox=self.component.data_bbox)

    def _get_end_xy_offset(self, component):
        return np.array([0, component.screen_bbox.height])
