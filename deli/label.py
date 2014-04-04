""" Defines the Label class.
"""
from math import pi

from enable.api import black_color_trait, transparent_color_trait
from kiva.trait_defs.kiva_font_trait import KivaFont
from traits.api import Any, Bool, Float, HasTraits, Int, List, Str


class Label(HasTraits):
    """ A label used by overlays.

    Label is not a Component; it's just an object encapsulating text settings
    and appearance attributes.  It can be used by components that need text
    labels to store state, perform layout, and render the text.
    """

    # The label text.  Carriage returns (\n) are always connverted into
    # line breaks.
    text = Str

    # The angle of rotation of the label.
    rotate_angle = Float(0)

    # The color of the label text.
    color = black_color_trait

    # The background color of the label.
    bgcolor = transparent_color_trait

    # The width of the label border. If it is 0, then it is not shown.
    border_width = Int(0)

    # The color of the border.
    border_color = black_color_trait

    # Whether or not the border is visible
    border_visible = Bool(True)

    # The font of the label text.
    font = KivaFont("modern 10")

    # Number of pixels of margin around the label, for both X and Y dimensions.
    margin = Int(2)

    # Number of pixels of spacing between lines of text.
    line_spacing = Int(5)

    max_width = Float(0.0)

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    _bounding_box = List()
    _position_cache_valid = Bool(False)
    _text_needs_fitting = Bool(True)
    _line_xpos = Any()
    _line_ypos = Any()

    def __init__(self, **traits):
        super(Label, self).__init__(**traits)
        self._bounding_box = [0, 0]
        return

    def get_width_height(self, gc):
        """ Returns the width and height of the label, in the rotated frame of
        reference.
        """
        self._fit_text_to_max_width(gc)
        self._calc_line_positions(gc)
        width, height = self._bounding_box
        return width, height

    def get_bounding_box(self, gc):
        """ Returns a rectangular bounding box for the Label as (width,height).
        """
        return self.get_width_height(gc)

    def draw(self, gc):
        """ Draws the label.

        This method assumes the graphics context has been translated to the
        correct position such that the origin is at the lower left-hand corner
        of this text label's box.
        """
        # Make sure `max_width` is respected
        self._fit_text_to_max_width(gc)

        # For this version we're not supporting rotated text.
        self._calc_line_positions(gc)

        with gc:
            bb_width, bb_height = self.get_bounding_box(gc)

            # Rotate label about center of bounding box
            width, height = self._bounding_box
            gc.translate_ctm(bb_width/2.0, bb_height/2.0)
            gc.rotate_ctm(pi/180.0*self.rotate_angle)
            gc.translate_ctm(-width/2.0, -height/2.0)

            gc.set_fill_color(self.color_)
            gc.set_stroke_color(self.color_)
            gc.set_font(self.font)
            gc.set_antialias(1)

            lines = self.text.split("\n")
            if self.border_visible:
                gc.translate_ctm(self.border_width, self.border_width)
            width, height = self.get_width_height(gc)

            for i, line in enumerate(lines):
                x_offset = round(self._line_xpos[i])
                y_offset = round(self._line_ypos[i])
                gc.set_text_position(x_offset, y_offset)
                gc.show_text(line)

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _fit_text_to_max_width(self, gc):
        """ Break the text into lines whose width is no greater than
        `max_width`.
        """
        if self._text_needs_fitting:
            lines = []

            with gc:
                gc.set_font(self.font)
                for line in self.text.split('\n'):
                    width = gc.get_full_text_extent(line)[0]
                    line_words = []
                    for word in line.split():
                        line_words.append(word)
                        test_line = ' '.join(line_words)
                        width = gc.get_full_text_extent(test_line)[0]
                        if width > self.max_width:
                            lines.append(word)
                            line_words = []
            self.trait_setq(text='\n'.join(lines))
            self._text_needs_fitting = False

    def _calc_line_positions(self, gc):
        if not self._position_cache_valid:
            with gc:
                gc.set_font(self.font)
                # The bottommost line starts at postion (0, 0).
                x_pos = []
                y_pos = []
                self._bounding_box = [0, 0]
                margin = self.margin
                prev_y_pos = margin
                prev_y_height = -self.line_spacing
                max_width = 0
                for line in self.text.split("\n")[::-1]:
                    if line != "":
                        (width, height, descent, leading) = \
                            gc.get_full_text_extent(line)
                        ascent = height - abs(descent)
                        if width > max_width:
                            max_width = width
                        new_y_pos = prev_y_pos + prev_y_height \
                            + self.line_spacing
                    x_pos.append(-leading + margin)
                    y_pos.append(new_y_pos)
                    prev_y_pos = new_y_pos
                    prev_y_height = ascent

            self._line_xpos = x_pos[::-1]
            self._line_ypos = y_pos[::-1]
            border_width = self.border_width if self.border_visible else 0
            self._bounding_box[0] = max_width + 2*margin + 2*border_width
            self._bounding_box[1] = prev_y_pos + prev_y_height + margin \
                + 2*border_width
            self._position_cache_valid = True
        return
