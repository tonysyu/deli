from enable.api import ColorTrait
from enable.markers import AbstractMarker, MarkerNameDict, marker_trait
from traits.api import (Float, HasStrictTraits, Instance, Int, Property,
                        cached_property)

from kiva.constants import STROKE


class MarkerArtist(HasStrictTraits):
    """ A Flyweight object for drawing markers.
    """

    #: The type of marker to use for the points
    marker = marker_trait

    _marker = Property(Instance(AbstractMarker), depends_on='marker')

    size = Int(5)

    edge_width = Float(1)

    edge_color = ColorTrait('black')

    fill_color = ColorTrait('yellow')

    @cached_property
    def _get__marker(self):
        if isinstance(self.marker, basestring):
            return MarkerNameDict[self.marker]()
        else:
            return self.marker()

    def update_style(self, gc):
        gc.set_line_dash(None)
        gc.set_stroke_color(self.edge_color_)
        gc.set_line_width(self.edge_width)
        if self._marker.draw_mode != STROKE:
            gc.set_fill_color(self.fill_color_)

    def draw(self, gc, points):
        """ Draw a series of markers points.

        Parameters
        ----------
        gc : GraphicsContext
            The graphics context where elements are drawn.
        points : array, shape (N, 2)
            Draw markers at these (x, y) points.
        """
        if len(points) == 0:
            return

        with gc:
            gc.draw_marker_at_points(points, self.size,
                                     self._marker.kiva_marker)
