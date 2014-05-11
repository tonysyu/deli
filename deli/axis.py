""" Defines the XAxis and YAxis classes.
"""
import numpy as np
from matplotlib.transforms import blended_transform_factory, IdentityTransform

from traits.api import DelegatesTo, Instance, Property, cached_property

from .abstract_overlay import AbstractOverlay
from .artist.label_artist import LabelArtist
from .artist.tick_artist import XTickArtist, YTickArtist
from .artist.tick_label_artist import XTickLabelArtist, YTickLabelArtist
from .artist.line_artist import LineArtist
from .layout.bbox_transform import BaseTransform, BboxTransform
from .layout.grid_layout import BaseGridLayout, XGridLayout, YGridLayout
from .style import config
from .utils.drawing import broadcast_points


class BaseAxis(AbstractOverlay):

    # A tick grid that controls tick positioning
    tick_grid = Instance(BaseGridLayout)

    #: Transform from data-space to screen-space.
    data_to_screen = Instance(BaseTransform)

    #------------------------------------------------------------------------
    # Appearance traits
    #------------------------------------------------------------------------

    #: Artist responsible for drawing tick labels.
    tick_label_artist = Instance(LabelArtist)

    #: Artist responsible for drawing ticks.
    tick_artist = Instance(LineArtist)

    #: Artist responsible for drawing the axis line.
    line_artist = Instance(LineArtist)

    #------------------------------------------------------------------------
    # Private Traits
    #------------------------------------------------------------------------

    #: XXX Maybe rename data-to-screen to axial transform?
    #: Transform from axial values to screen-space.
    # axial_transform = Instance(BaseTransform)

    #: Transform from values orthogonal to the axis to screen-space.
    ortho_transform = Instance(BaseTransform, IdentityTransform())

    #: Blended transform combining axial and orthogonal transforms.
    transform = Property(Instance(BaseTransform))

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
        with gc:
            self._draw_axis_line(gc)
            self._draw_ticks(gc)
            self._draw_labels(gc)

    #------------------------------------------------------------------------
    # Private draw routines
    #------------------------------------------------------------------------

    def _draw_axis_line(self, gc):
        """ Draws the line for the axis. """
        xy_axis_min, xy_axis_max = self._compute_xy_end_points()
        self.line_artist.update_style(gc)
        self.line_artist.draw_segments(gc, xy_axis_min, xy_axis_max)

    def _draw_ticks(self, gc):
        """ Draws the tick marks for the axis.
        """
        self.tick_artist.update_style(gc)
        self.tick_artist.draw(gc, self.tick_grid.axial_offsets)

    def _draw_labels(self, gc):
        """ Draws the tick labels for the axis.
        """
        axial_offsets = self.tick_grid.axial_offsets
        xy_tick = self._get_tick_positions()
        for xy_screen, data_offset in zip(xy_tick, axial_offsets):
            gc.translate_ctm(*xy_screen)
            self.tick_label_artist.draw(gc, str(data_offset))
            gc.translate_ctm(*(-xy_screen))

    #------------------------------------------------------------------------
    # Private methods for computing positions and layout
    #------------------------------------------------------------------------

    def _compute_xy_end_points(self):
        end_xy_offset = self._get_end_xy_offset(self.component)
        xy_axis_min = np.array([self.component.x, self.component.y])
        xy_axis_max = end_xy_offset + xy_axis_min
        return xy_axis_min, xy_axis_max

    def _data_to_screen_default(self):
        component = self.component
        return BboxTransform(component.data_bbox, component.screen_bbox)


class XAxis(BaseAxis):

    locus = DelegatesTo('component', 'y')

    def _line_artist_default(self):
        return LineArtist(color=config.get('axis.line.color'))

    def _tick_artist_default(self):
        return XTickArtist(color=config.get('axis.tick.color'),
                           locus=self.locus,
                           transform=self.transform)

    def _tick_label_artist_default(self):
        return XTickLabelArtist(offset=-config.get('axis.tick_label.offset'),
                                color=config.get('axis.tick_label.color'))

    def _tick_grid_default(self):
        return XGridLayout(data_bbox=self.component.data_bbox)

    @cached_property
    def _get_transform(self):
        return blended_transform_factory(self.data_to_screen,
                                         self.ortho_transform)

    def _get_end_xy_offset(self, component):
        return np.array([component.screen_bbox.width, 0])

    def _get_tick_positions(self):
        points = broadcast_points(self.tick_grid.axial_offsets, self.locus)
        return self.transform.transform(points)


class YAxis(BaseAxis):

    locus = DelegatesTo('component', 'x')

    def _line_artist_default(self):
        return LineArtist(color=config.get('axis.line.color'))

    def _tick_artist_default(self):
        return YTickArtist(color=config.get('axis.tick.color'),
                           locus=self.locus,
                           transform=self.transform)

    def _tick_label_artist_default(self):
        return YTickLabelArtist(offset=-config.get('axis.tick_label.offset'),
                                color=config.get('axis.tick_label.color'))

    def _tick_grid_default(self):
        return YGridLayout(data_bbox=self.component.data_bbox)

    @cached_property
    def _get_transform(self):
        return blended_transform_factory(self.ortho_transform,
                                         self.data_to_screen)

    def _get_end_xy_offset(self, component):
        return np.array([0, component.screen_bbox.height])

    def _get_tick_positions(self):
        points = broadcast_points(self.locus, self.tick_grid.axial_offsets)
        return self.transform.transform(points)
