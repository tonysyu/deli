from abc import abstractmethod

import numpy as np
from traits.api import Float, Instance, Property

from ..layout.bbox_transform import BaseTransform
from ..style import config
from .line_stylus import LineStylus


def offsets_to_points(axial_offsets, axial_coordinate, locus=0):
    if axial_coordinate == 'x':
        points = [axial_offsets, locus]
    else:
        points = [locus, axial_offsets]
    return np.transpose(np.broadcast_arrays(*points))


class BaseTickStylus(LineStylus):

    #: The screen position of the axis in the dimension that's fixed;
    #: i.e. x-position for a y-axis and y-position for an x-axis.
    locus = Float(0)

    in_size = Float(config.get('in.tick_size'))

    out_size = Float(config.get('out.tick_size'))

    size = Property

    #: Blended transform combining axial and orthogonal transforms.
    transform = Instance(BaseTransform)

    def _set_size(self, value):
        self.in_size = value
        self.out_size = value

    def draw(self, gc, offsets):
        tick_segments = self._offsets_to_segments(offsets)
        self.draw_segments(gc, *tick_segments)

    @abstractmethod
    def _offsets_to_segments(self, offsets):
        """ Return starting and ending points from positions. """


class XTickStylus(BaseTickStylus):
    """ A Flyweight object for drawing x-ticks.
    """

    def _offsets_to_segments(self, offsets):
        points = offsets_to_points(offsets, 'x', locus=self.locus)
        centers = self.transform.transform(points)
        starts = centers + [0, self.in_size]
        ends = centers - [0, self.out_size]
        return starts, ends


class YTickStylus(BaseTickStylus):
    """ A Flyweight object for drawing y-ticks.
    """

    def _offsets_to_segments(self, offsets):
        points = offsets_to_points(offsets, 'y', locus=self.locus)
        centers = self.transform.transform(points)
        starts = centers + [self.in_size, 0]
        ends = centers - [self.out_size, 0]
        return starts, ends
