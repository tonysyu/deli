from enable.api import ColorTrait
from traits.api import HasStrictTraits, Instance

from .label_artist import LabelArtist


DEFAULT_LABEL_STYLE = {'x_origin': 'left', 'x_offset': 20, 'margin': 5}


class FlagArtist(HasStrictTraits):

    fill_color = ColorTrait('yellow')
    edge_color = ColorTrait('black')

    def draw(self, gc, rect, origin=(0, 0)):
        with gc:
            if self.fill_color is not 'none':
                gc.set_fill_color(self.fill_color_)
                gc.lines(self._poly_vertices(origin, rect))
                gc.fill_path()
            if self.edge_color is not 'none':
                gc.set_stroke_color(self.edge_color_)
                gc.lines(self._poly_vertices(origin, rect))
                gc.close_path()
                gc.stroke_path()

    def _poly_vertices(self, origin, rect):
        x, y, width, height = rect
        return [origin,
                (x, y),
                (x + width, y),
                (x + width, y + height),
                (x, y + height)]


class FlagLabelArtist(HasStrictTraits):

    text_color = ColorTrait('black')

    label = Instance(LabelArtist, DEFAULT_LABEL_STYLE)
    flag = Instance(FlagArtist, ())

    def draw(self, gc, text):
        """ Draw the given text with a flag-label decoration.

        Parameters
        ----------
        gc : GraphicsContext
            The graphics context where elements are drawn.
        text : str
            The text for the displayed label.
        """
        width, height = self.label.get_size(gc, text)

        x_bbox_offset = (self.label._x_offset_factor * width
                         + self.label.x_offset)
        y_bbox_offset = (self.label._y_offset_factor * height
                         + self.label.y_offset)

        rect = (x_bbox_offset, y_bbox_offset, width, height)
        self.flag.draw(gc, rect)
        self.label.draw(gc, text)
