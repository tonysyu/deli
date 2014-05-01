from abc import abstractmethod

import numpy as np
from matplotlib.transforms import blended_transform_factory, IdentityTransform
from traits.api import cached_property, Float, Instance, Property

from ..layout.bbox_transform import BaseTransform
from .line_artist import LineArtist


def offsets_to_points(axial_offsets, axial_coordinate, locus=0):
    if axial_coordinate == 'x':
        points = [axial_offsets, locus]
    else:
        points = [locus, axial_offsets]
    return np.transpose(np.broadcast_arrays(*points))


class BaseTickArtist(LineArtist):

    #: The position of the axis in the dimension that's fixed;
    #: i.e. x-position for a y-axis and y-position for an x-axis.
    locus = Float(0)

    in_size = Float(5.0)

    out_size = Float(5.0)

    size = Property

    #: Transform from axial values to screen-space.
    axial_transform = Instance(BaseTransform)

    #: Transform from values orthogonal to the axis to screen-space.
    ortho_transform = Instance(BaseTransform, IdentityTransform())

    #: Blended transform combining axial and orthogonal transforms.
    _transform = Property(Instance(BaseTransform))

    def _set_size(self, value):
        self.in_size = value
        self.out_size = value

    def draw(self, gc, offsets):
        tick_segments = self._offsets_to_segments(offsets)
        self.draw_segments(gc, *tick_segments)

    @abstractmethod
    def _offsets_to_segments(self, offsets):
        """ Return starting and ending points from positions. """


class XTickArtist(BaseTickArtist):
    """ A Flyweight object for drawing x-ticks.
    """

    @cached_property
    def _get__transform(self):
        return blended_transform_factory(self.axial_transform,
                                         self.ortho_transform)

    def _offsets_to_segments(self, offsets):
        points = offsets_to_points(offsets, 'x', locus=self.locus)
        centers = self._transform.transform(points)
        starts = centers + [0, self.in_size]
        ends = centers - [0, self.out_size]
        return starts, ends


class YTickArtist(BaseTickArtist):
    """ A Flyweight object for drawing y-ticks.
    """

    @cached_property
    def _get__transform(self):
        return blended_transform_factory(self.ortho_transform,
                                         self.axial_transform)

    def _offsets_to_segments(self, offsets):
        points = offsets_to_points(offsets, 'y', locus=self.locus)
        centers = self._transform.transform(points)
        starts = centers + [self.in_size, 0]
        ends = centers - [self.out_size, 0]
        return starts, ends
