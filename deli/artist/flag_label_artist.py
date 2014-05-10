from enable.api import ColorTrait
from traits.api import HasStrictTraits, Instance, Property

from .label_artist import LabelArtist
from .polygon_artist import PolygonArtist


DEFAULT_LABEL_STYLE = {'x_origin': 'left', 'x_offset': 20, 'margin': 5}


class FlagArtist(PolygonArtist):

    def draw(self, gc, rect, origin=(0, 0)):
        vertices = self._poly_vertices(origin, rect)
        super(FlagArtist, self).draw(gc, vertices)

    def _poly_vertices(self, origin, rect):
        x, y, width, height = rect
        return [origin,
                (x, y),
                (x + width, y),
                (x + width, y + height),
                (x, y + height)]


class FlagLabelArtist(HasStrictTraits):

    text_color = Property(ColorTrait)
    fill_color = Property(ColorTrait)
    edge_color = Property(ColorTrait)

    label = Instance(LabelArtist, DEFAULT_LABEL_STYLE)
    flag = Instance(FlagArtist, ())

    def _set_text_color(self, value):
        self.label.color = value

    def _set_fill_color(self, value):
        self.flag.fill_color = value

    def _set_edge_color(self, value):
        self.flag.edge_color = value

    def draw(self, gc, text):
        """ Draw the given text with a flag-label decoration.

        Parameters
        ----------
        gc : GraphicsContext
            The graphics context where elements are drawn.
        text : str
            The text for the displayed label.
        """
        x, y, width, height = self.label.text_rect(gc, text)
        x_offset, y_offset = self.label.bbox_offset(gc, text, width, height)
        rect = (x_offset, y_offset, width, height)

        self.flag.draw(gc, rect)
        self.label.draw(gc, text)
