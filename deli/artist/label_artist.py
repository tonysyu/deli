""" Defines the Label class.
"""
from math import pi

from enable.api import black_color_trait, transparent_color_trait
from kiva.trait_defs.kiva_font_trait import KivaFont
from traits.api import (Any, Bool, Enum, Float, HasStrictTraits, Int, List,
                        Property, Str, cached_property)


class LabelArtist(HasStrictTraits):
    """ A Flyweight object for drawing text labels.
    """

    # The label text.
    text = Str

    # The angle of rotation (in degrees) of the label.
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

    x_origin = Enum('center', 'left', 'right')
    y_origin = Enum('center', 'bottom', 'top')

    _x_offset_factor = Property(Int, depends_on='x_origin')
    _y_offset_factor = Property(Int, depends_on='y_origin')

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    _size = List()
    _line_xpos = Any()
    _line_ypos = Any()

    def __init__(self, **traits):
        super(LabelArtist, self).__init__(**traits)
        self._size = [0, 0]

    def get_size(self, gc, text):
        """ Returns the label size as (width, height).
        """
        self._calc_line_positions(gc, text)
        return self._size

    def update_context(self, gc):
        gc.set_fill_color(self.color_)
        gc.set_stroke_color(self.color_)
        gc.set_font(self.font)
        gc.set_antialias(True)

    def set_rotation_angle(self, gc, text):
        bb_width, bb_height = self.get_size(gc, text)
        width, height = self._size

        # Rotate label about center of bounding box
        gc.translate_ctm(bb_width / 2.0, bb_height / 2.0)
        gc.rotate_ctm(pi / 180.0 * self.rotate_angle)
        gc.translate_ctm(-width / 2.0, -height / 2.0)

    def draw(self, gc, text):
        """ Draws the label.

        This method assumes the graphics context has been translated to the
        correct position such that the origin is at the lower left-hand corner
        of this text label's box.
        """
        # For this version we're not supporting rotated text.
        self._calc_line_positions(gc, text)

        with gc:
            self.update_context(gc)
            self.set_rotation_angle(gc, text)

            lines = text.split("\n")
            if self.border_visible:
                gc.translate_ctm(self.border_width, self.border_width)
            width, height = self.get_size(gc, text)

            x_bbox_offset = self._x_offset_factor * width
            y_bbox_offset = self._y_offset_factor * height

            for i, line in enumerate(lines):
                x_offset = round(self._line_xpos[i]) + x_bbox_offset
                y_offset = round(self._line_ypos[i]) + y_bbox_offset
                gc.set_text_position(x_offset, y_offset)
                gc.show_text(line)

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    @cached_property
    def _get__x_offset_factor(self):
        # Fraction of label bounding-box width used to shift origin.
        if self.x_origin == 'center':
            return -0.5
        elif self.x_origin == 'left':
            return 0
        elif self.x_origin == 'right':
            return -1

    @cached_property
    def _get__y_offset_factor(self):
        # Fraction of label bounding-box height used to shift origin.
        if self.y_origin == 'center':
            return -0.5
        elif self.y_origin == 'top':
            return -1
        elif self.y_origin == 'bottom':
            return 0

    def _calc_line_positions(self, gc, text):
        with gc:
            gc.set_font(self.font)
            # The bottommost line starts at postion (0, 0).
            x_pos = []
            y_pos = []
            margin = self.margin
            prev_y_pos = margin
            prev_y_height = -self.line_spacing
            max_width = 0
            for line in text.split("\n")[::-1]:
                if len(line) > 0:
                    text_extent = gc.get_full_text_extent(line)
                    (width, height, descent, leading) = text_extent
                    ascent = height - abs(descent)
                    if width > max_width:
                        max_width = width
                    new_y_pos = prev_y_pos + prev_y_height + self.line_spacing
                x_pos.append(-leading + margin)
                y_pos.append(new_y_pos)
                prev_y_pos = new_y_pos
                prev_y_height = ascent

        self._line_xpos = x_pos[::-1]
        self._line_ypos = y_pos[::-1]
        border_width = self.border_width if self.border_visible else 0
        self._size[0] = max_width + 2*margin + 2*border_width
        self._size[1] = prev_y_pos + prev_y_height + margin \
            + 2*border_width
