""" Defines the XGrid and YGrid classes.
"""
import numpy as np

from traits.api import Array, Instance, on_trait_change

from .abstract_overlay import AbstractOverlay
from .artist.line_artist import LineArtist
from .layout.grid_layout import BaseGridLayout, XGridLayout, YGridLayout
from .utils.drawing import hline_segments, vline_segments


class BaseGrid(AbstractOverlay):
    """ An overlay that represents a grid.

    A grid is a set of parallel lines, horizontal or vertical. You can use
    multiple grids with different settings for the horizontal and vertical
    lines in a plot.
    """

    # A tick grid that controls tick positioning
    tick_grid = Instance(BaseGridLayout)

    #------------------------------------------------------------------------
    # Appearance traits
    #------------------------------------------------------------------------

    line_artist = Instance(LineArtist)

    def _line_artist_default(self):
        return LineArtist(color='lightgray', style='dot')

    # Set default background color to transparent.
    bgcolor = 'none'

    #------------------------------------------------------------------------
    # Private traits; mostly cached information
    #------------------------------------------------------------------------

    _line_starts = Array
    _line_ends = Array

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    @on_trait_change("bounds,bounds_items,position,position_items")
    def invalidate(self):
        """ Invalidate cached information about the grid.
        """
        self._reset_cache()

    #--------------------------------------------------------------------------
    #  Protected interface
    #--------------------------------------------------------------------------

    def _compute_ticks(self, component):
        raise NotImplementedError()

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _reset_cache(self):
        """ Clears the cached tick positions.
        """
        self._line_starts = np.array([])
        self._line_ends = np.array([])

    def draw(self, other_component, gc, view_bounds=None):
        """ Draws this component overlaid on another component.

        Overrides AbstractOverlay.
        """
        other_component = getattr(other_component, 'canvas', other_component)
        self._compute_ticks(other_component)
        self._draw_component(gc, view_bounds)

    def _draw_component(self, gc, view_bounds=None):
        """ Draws the component.

        This method is preserved for backwards compatibility. Overrides
        Component.
        """
        with gc:
            self.line_artist.update_style(gc)
            gc.set_antialias(False)
            gc.clip_to_rect(*(self.component.position + self.component.bounds))
            self.line_artist.draw_segments(gc, self._line_starts,
                                               self._line_ends)

    def _position_changed_for_component(self):
        self.invalidate()

    def _bounds_changed_for_component(self):
        self.invalidate()

    #------------------------------------------------------------------------
    # Event handlers for visual attributes.
    #------------------------------------------------------------------------

    @on_trait_change("visible,line_color,line_style,line_width")
    def _visual_attr_changed(self):
        """ Called when an attribute that affects the appearance of the grid
        is changed.
        """
        self.component.request_redraw()

    def _orientation_changed(self):
        self.invalidate()
        self._visual_attr_changed()


class XGrid(BaseGrid):

    def _tick_grid_default(self):
        return XGridLayout(data_bbox=self.component.data_bbox)

    def _compute_ticks(self, component):
        """ Calculate the positions of grid lines in screen space.
        """
        offsets = self.tick_grid.axial_offsets
        y_lo, y_hi = component.screen_bbox.y_limits

        y = np.resize(y_lo, offsets.shape)
        points = np.transpose((offsets, y))
        offsets = component.data_to_screen.transform(points)[:, 0]

        starts, ends = vline_segments(offsets, y_lo, y_hi)

        self._line_starts = np.around(starts)
        self._line_ends = np.around(ends)


class YGrid(BaseGrid):

    def _tick_grid_default(self):
        return YGridLayout(data_bbox=self.component.data_bbox)

    def _compute_ticks(self, component):
        """ Calculate the positions of grid lines in screen space.
        """
        offsets = self.tick_grid.axial_offsets
        x_lo, x_hi = component.screen_bbox.x_limits

        x = np.resize(x_lo, offsets.shape)
        points = np.transpose((x, offsets))
        offsets = component.data_to_screen.transform(points)[:, 1]

        starts, ends = hline_segments(offsets, x_lo, x_hi)

        self._line_starts = np.around(starts)
        self._line_ends = np.around(ends)
