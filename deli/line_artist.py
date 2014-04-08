from enable.api import ColorTrait, LineStyle
from traits.api import HasStrictTraits, CFloat


class LineArtist(HasStrictTraits):

    # The color of the grid lines.
    color = ColorTrait('black')

    # The style (i.e., dash pattern) of the grid lines.
    style = LineStyle('solid')

    # The thickness, in pixels, of the grid lines.
    width = CFloat(1)

    def update_context(self, gc):
        gc.set_line_width(self.width)
        gc.set_line_dash(self.style_)
        gc.set_stroke_color(self.color_)
