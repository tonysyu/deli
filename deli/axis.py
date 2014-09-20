""" Defines the XAxis and YAxis classes.
"""
import numpy as np

from traits.api import (Float, Instance, Property, cached_property,
                        on_trait_change)

from .abstract_overlay import AbstractOverlay
from .stylus.label_stylus import LabelStylus
from .stylus.tick_stylus import XTickStylus, YTickStylus
from .stylus.tick_label_stylus import XTickLabelStylus, YTickLabelStylus
from .stylus.line_stylus import LineStylus
from .stylus.segment_stylus import SegmentStylus
from .layout.bbox_transform import (
    BaseTransform, BboxTransform, IdentityTransform, blend_xy_transforms
)
from .layout.grid_layout import BaseGridLayout, XGridLayout, YGridLayout
from .style import config
from .utils.drawing import broadcast_points


class BaseAxis(AbstractOverlay):

    # A tick grid that controls tick positioning
    tick_grid = Instance(BaseGridLayout)

    #: Transform from data-space to screen-space.
    data_to_screen = Instance(BaseTransform)

    # -----------------------------------------------------------------------
    # Appearance traits
    # -----------------------------------------------------------------------

    #: Stylus responsible for drawing tick labels.
    tick_label_stylus = Instance(LabelStylus)

    #: Stylus responsible for drawing ticks.
    tick_stylus = Instance(LineStylus)

    #: Stylus responsible for drawing the axis line.
    line_stylus = Instance(SegmentStylus)

    # -----------------------------------------------------------------------
    # Private Traits
    # -----------------------------------------------------------------------

    #: XXX Maybe rename data-to-screen to axial transform?
    #: Transform from axial values to screen-space.
    # axial_transform = Instance(BaseTransform)

    #: Transform from values orthogonal to the axis to screen-space.
    ortho_transform = Instance(BaseTransform, IdentityTransform())

    #: Blended transform combining axial and orthogonal transforms.
    transform = Property(Instance(BaseTransform))

    # -------------------------------------------------------------------------
    #  Protected interface
    # -------------------------------------------------------------------------

    locus = Float(0)

    @on_trait_change('component.origin')
    def _update_locus(self):
        self.tick_stylus.locus = self.locus

    # -----------------------------------------------------------------------
    # Public interface
    # -----------------------------------------------------------------------

    def data_offset_to_label(self, data_offset):
        return str(data_offset)

    # -----------------------------------------------------------------------
    # Component and AbstractOverlay interface
    # -----------------------------------------------------------------------

    def draw(self, gc, view_rect=None):
        """ Draws this component overlaid on another component. """
        with gc:
            self._draw_axis_line(gc)
            self._draw_ticks(gc)
            self._draw_labels(gc)

    # -----------------------------------------------------------------------
    # Private draw routines
    # -----------------------------------------------------------------------

    def _draw_axis_line(self, gc):
        """ Draws the line for the axis. """
        xy_axis_min, xy_axis_max = self._compute_xy_end_points()
        self.line_stylus.draw(gc, xy_axis_min, xy_axis_max)

    def _draw_ticks(self, gc):
        """ Draws the tick marks for the axis.
        """
        self.tick_stylus.draw(gc, self.tick_grid.axial_offsets)

    def _draw_labels(self, gc):
        """ Draws the tick labels for the axis.
        """
        axial_offsets = self.tick_grid.axial_offsets
        xy_tick = self._get_tick_positions()
        for xy_screen, data_offset in zip(xy_tick, axial_offsets):
            gc.translate_ctm(*xy_screen)
            label = self.data_offset_to_label(data_offset)
            self.tick_label_stylus.draw(gc, label)
            gc.translate_ctm(*(-xy_screen))

    # -----------------------------------------------------------------------
    # Private methods for computing positions and layout
    # -----------------------------------------------------------------------

    def _compute_xy_end_points(self):
        end_xy_offset = self._get_end_xy_offset(self.component)
        xy_axis_min = np.array([0, 0])
        xy_axis_max = end_xy_offset + xy_axis_min
        return xy_axis_min, xy_axis_max

    def _data_to_screen_default(self):
        component = self.component
        return BboxTransform(component.data_bbox, component.local_bbox)


class XAxis(BaseAxis):

    def _line_stylus_default(self):
        return SegmentStylus(color=config.get('axis.line.color'))

    def _tick_stylus_default(self):
        return XTickStylus(color=config.get('axis.tick.color'),
                           locus=self.locus,
                           transform=self.transform)

    def _tick_label_stylus_default(self):
        return XTickLabelStylus(offset=-config.get('axis.tick_label.offset'),
                                color=config.get('axis.tick_label.color'))

    def _tick_grid_default(self):
        return XGridLayout(data_bbox=self.component.data_bbox)

    @cached_property
    def _get_transform(self):
        return blend_xy_transforms(self.data_to_screen, self.ortho_transform)

    def _get_end_xy_offset(self, component):
        return np.array([component.local_bbox.width, 0])

    def _get_tick_positions(self):
        points = broadcast_points(self.tick_grid.axial_offsets, self.locus)
        return self.transform.transform(points)


class YAxis(BaseAxis):

    def _line_stylus_default(self):
        return SegmentStylus(color=config.get('axis.line.color'))

    def _tick_stylus_default(self):
        return YTickStylus(color=config.get('axis.tick.color'),
                           locus=self.locus,
                           transform=self.transform)

    def _tick_label_stylus_default(self):
        return YTickLabelStylus(offset=-config.get('axis.tick_label.offset'),
                                color=config.get('axis.tick_label.color'))

    def _tick_grid_default(self):
        return YGridLayout(data_bbox=self.component.data_bbox)

    @cached_property
    def _get_transform(self):
        return blend_xy_transforms(self.ortho_transform, self.data_to_screen)

    def _get_end_xy_offset(self, component):
        return np.array([0, component.local_bbox.height])

    def _get_tick_positions(self):
        points = broadcast_points(self.locus, self.tick_grid.axial_offsets)
        return self.transform.transform(points)
