""" Defines the XGrid and YGrid classes.
"""
import numpy as np

from traits.api import Array, Instance, on_trait_change

from .artist.base_artist import BaseArtist
from .stylus.segment_stylus import SegmentStylus
from .layout.grid_layout import BaseGridLayout, XGridLayout, YGridLayout
from .layout.bbox_transform import BboxTransform
from .utils.drawing import hline_segments, vline_segments


class BaseGrid(BaseArtist):
    """ An artist that draws a grid.

    A grid is a set of parallel lines, horizontal or vertical. You can use
    multiple grids with different settings for the horizontal and vertical
    lines in a plot.
    """

    # A tick grid that controls tick positioning
    tick_grid = Instance(BaseGridLayout)

    # -----------------------------------------------------------------------
    # Appearance traits
    # -----------------------------------------------------------------------

    line_stylus = Instance(SegmentStylus)

    def _line_stylus_default(self):
        # XXX: Replace these defaults with config values.
        return SegmentStylus(color='lightgray', style='dot')

    # -----------------------------------------------------------------------
    # Private traits; mostly cached information
    # -----------------------------------------------------------------------

    _line_starts = Array
    _line_ends = Array

    # -----------------------------------------------------------------------
    # Public methods
    # -----------------------------------------------------------------------

    @on_trait_change("size,size_items,origin,origin_items")
    def invalidate(self):
        """ Invalidate cached information about the grid. """
        self._reset_cache()

    # -------------------------------------------------------------------------
    #  Protected interface
    # -------------------------------------------------------------------------

    def _compute_ticks(self):
        raise NotImplementedError()

    # -----------------------------------------------------------------------
    # Private methods
    # -----------------------------------------------------------------------

    def _reset_cache(self):
        """ Clears the cached tick positions. """
        self._line_starts = np.array([])
        self._line_ends = np.array([])

    def draw(self, gc, view_rect=None):
        """ Draws this component overlaid on another component. """
        self._compute_ticks()
        with gc:
            gc.set_antialias(False)
            gc.clip_to_rect(*([0, 0] + self.size))
            self.line_stylus.draw(gc, self._line_starts, self._line_ends)

    def _origin_changed_for_component(self):
        self.invalidate()

    def _size_changed_for_component(self):
        self.invalidate()

    # -----------------------------------------------------------------------
    # Event handlers for visual attributes.
    # -----------------------------------------------------------------------

    @on_trait_change("visible,line_color,line_style,line_width")
    def _visual_attr_changed(self):
        self.container.request_redraw()

    def _orientation_changed(self):
        self.invalidate()
        self._visual_attr_changed()

    def _data_to_screen_default(self):
        return BboxTransform(self.data_bbox, self.screen_bbox)


class XGrid(BaseGrid):

    def _tick_grid_default(self):
        return XGridLayout(data_bbox=self.data_bbox)

    def _compute_ticks(self):
        """ Calculate the positions of grid lines in screen space. """
        offsets = self.tick_grid.axial_offsets
        y_lo, y_hi = self.screen_bbox.y_limits

        y = np.resize(y_lo, offsets.shape)
        points = np.transpose((offsets, y))
        offsets = self.data_to_screen.transform(points)[:, 0]

        starts, ends = vline_segments(offsets, y_lo, y_hi)

        self._line_starts = np.around(starts)
        self._line_ends = np.around(ends)


class YGrid(BaseGrid):

    def _tick_grid_default(self):
        return YGridLayout(data_bbox=self.data_bbox)

    def _compute_ticks(self):
        """ Calculate the positions of grid lines in screen space. """
        offsets = self.tick_grid.axial_offsets
        x_lo, x_hi = self.screen_bbox.x_limits

        x = np.resize(x_lo, offsets.shape)
        points = np.transpose((x, offsets))
        offsets = self.data_to_screen.transform(points)[:, 1]

        starts, ends = hline_segments(offsets, x_lo, x_hi)

        self._line_starts = np.around(starts)
        self._line_ends = np.around(ends)
