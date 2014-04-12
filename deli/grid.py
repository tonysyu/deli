""" Defines the PlotGrid class, and associated Traits UI View and validator
function.
"""
import numpy as np

from traits.api import Array, Enum, Instance, on_trait_change

from .abstract_overlay import AbstractOverlay
from .abstract_mapper import AbstractMapper
from .line_artist import LineArtist
from .ticks import TickGrid
from .utils import hline_segments, switch_trait_handler, vline_segments


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

    # A callable that implements the AbstractTickGenerator Interface.
    tick_grid = Instance(TickGrid, ())

    #------------------------------------------------------------------------
    # Layout traits
    #------------------------------------------------------------------------

    # The orientation of the grid lines.  "horizontal" means that the grid
    # lines are parallel to the X axis and the ticker and grid interval
    # refer to the Y axis.
    orientation = Enum('horizontal', 'vertical')

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

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _reset_cache(self):
        """ Clears the cached tick positions.
        """
        self._line_starts = np.array([])
        self._line_ends = np.array([])

    def _compute_ticks(self, component):
        """ Calculate the positions of grid lines in screen space.
        """
        self.tick_grid.update(self.mapper)
        offsets = self.tick_grid.x_screen  # x = x or y, depending on grid.

        bounds = component.bounds
        position = component.position

        x_lo, y_lo = position
        x_hi = x_lo + bounds[0]
        y_hi = y_lo + bounds[1]

        if self.orientation == 'horizontal':
            starts, ends = hline_segments(offsets, x_lo, x_hi)
        elif self.orientation == 'vertical':
            starts, ends = vline_segments(offsets, y_lo, y_hi)

        self._line_starts = np.around(starts)
        self._line_ends = np.around(ends)

    def overlay(self, other_component, gc, view_bounds=None, mode="normal"):
        """ Draws this component overlaid on another component.

        Overrides AbstractOverlay.
        """
        self._compute_ticks(other_component)
        self._draw_component(gc, view_bounds, mode)

    def _draw_component(self, gc, view_bounds=None, mode="normal"):
        """ Draws the component.

        This method is preserved for backwards compatibility. Overrides
        PlotComponent.
        """
        with gc:
            self.line_artist.update_context(gc)
            gc.set_antialias(False)
            gc.clip_to_rect(*(self.component.position + self.component.bounds))

            gc.begin_path()

            gc.line_set(self._line_starts, self._line_ends)
            gc.stroke_path()

    def _mapper_changed(self, old, new):
        switch_trait_handler(old, new, 'updated', self._mapper_updated)
        self.invalidate()

    def _mapper_updated(self):
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

    @on_trait_change("visible,line_color,line_style,line_width")
    def _visual_attr_changed(self):
        """ Called when an attribute that affects the appearance of the grid
        is changed.
        """
        self.component.invalidate_draw()
        self.component.request_redraw()

    def _orientation_changed(self):
        self.invalidate()
        self._visual_attr_changed()
