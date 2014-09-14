from traits.api import DelegatesTo, Instance

from ..stylus.line_stylus import LineStylus
from .base_point_artist import BasePointArtist


class LineArtist(BasePointArtist):
    """ An artist for line data.
    """
    # The color of the line.
    color = DelegatesTo('line')

    line = Instance(LineStylus, ())

    #--------------------------------------------------------------------------
    #  Private interface
    #--------------------------------------------------------------------------

    def _render(self, gc, points, selected_points=None):
        with gc:
            gc.clip_to_rect(*self.screen_bbox.rect)
            self.line.draw(gc, points)

    def _color_changed(self):
        self.request_redraw()

    def _get_styluses(self):
        return (self.line,)
