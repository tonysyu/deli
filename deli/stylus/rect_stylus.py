from enable.api import ColorTrait

from .base_patch_stylus import BasePatchStylus


class RectangleStylus(BasePatchStylus):
    """ A Flyweight object for drawing filled rectangles.
    """

    edge_color = ColorTrait('black')

    fill_color = ColorTrait('yellow')

    def draw(self, gc, rect):
        with gc:
            gc.set_stroke_color(self.edge_color_)
            if self.fill_color is not 'none':
                gc.set_fill_color(self.fill_color_)
                gc.fill_path()
            gc.draw_rect([int(a) for a in rect])
