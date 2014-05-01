from abc import abstractmethod

import numpy as np
from matplotlib.transforms import blended_transform_factory, IdentityTransform
from traits.api import cached_property, Float, Instance, Property

from ..layout.bbox_transform import BaseTransform
from .line_artist import LineArtist


def offsets_to_points(axial_offsets, axial_coordinate, ortho_position=0):
    if axial_coordinate == 'x':
        points = [axial_offsets, ortho_position]
    else:
        points = [ortho_position, axial_offsets]
    return np.transpose(np.broadcast_arrays(*points))


class BaseTickArtist(LineArtist):

    position = Float(0)

    in_size = Float(5.0)

    out_size = Float(5.0)

    size = Property

    #: Transform from offset values to screen-space.
    offset_transform = Instance(BaseTransform)

    #: Transform from position value to screen-space.
    position_transform = Instance(BaseTransform, IdentityTransform())

    #: Blended transform combining position and offset transforms.
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
        return blended_transform_factory(self.offset_transform,
                                         self.position_transform)

    def _offsets_to_segments(self, offsets):
        points = offsets_to_points(offsets, 'x', ortho_position=self.position)
        centers = self._transform.transform(points)
        starts = centers + [0, self.in_size]
        ends = centers - [0, self.out_size]
        return starts, ends


class YTickArtist(BaseTickArtist):
    """ A Flyweight object for drawing y-ticks.
    """

    @cached_property
    def _get__transform(self):
        return blended_transform_factory(self.position_transform,
                                         self.offset_transform)

    def _offsets_to_segments(self, offsets):
        points = offsets_to_points(offsets, 'y', ortho_position=self.position)
        centers = self._transform.transform(points)
        starts = centers + [self.in_size, 0]
        ends = centers - [self.out_size, 0]
        return starts, ends
