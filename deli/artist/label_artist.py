""" Defines the Label class.
"""
from math import pi

from enable.api import ColorTrait
from kiva.trait_defs.kiva_font_trait import KivaFont
from traits.api import (Enum, Float, HasStrictTraits, Int, Property, Str,
                        cached_property)

from ..style import config


class LabelArtist(HasStrictTraits):
    """ A Flyweight object for drawing text labels.
    """

    #: The label text.
    text = Str

    #: The angle of rotation (in degrees) of the label.
    rotate_angle = Float(0)

    #: The color of the label text.
    color = ColorTrait(config.get('text.label.color'))

    #: The font of the label text.
    font = KivaFont(config.get('text.label.font'))

    #: Number of pixels of margin around the label, for both X and Y dimensions.
    margin = Int(config.get('label.margin'))

    #: Offset value from the current graphics-context position.
    x_offset = Float(0)
    y_offset = Float(0)

    #: Origin of the text label, which can be placed on edges and mid-points.
    x_origin = Enum('center', 'left', 'right')
    y_origin = Enum('center', 'bottom', 'top')

    #: Factor of width and height used to shift label to desired origin.
    _x_origin_factor = Property(Int, depends_on='x_origin')
    _y_origin_factor = Property(Int, depends_on='y_origin')

    def __init__(self, **traits):
        super(LabelArtist, self).__init__(**traits)

    def update_style(self, gc):
        gc.set_fill_color(self.color_)
        gc.set_stroke_color(self.color_)
        gc.set_font(self.font)
        gc.set_antialias(True)

    def draw(self, gc, text):
        """ Draws the label.

        This method assumes the graphics context has been translated to the
        correct position such that the origin is at the lower left-hand corner
        of this text label's box.
        """
        x, y, width, height = self.text_rect(gc, text)
        x_offset, y_offset = self.bbox_offset(gc, text, width, height)

        with gc:
            self.update_style(gc)
            self._set_rotation_angle(gc, text, width, height)

            gc.set_text_position(x + x_offset, y + y_offset)
            gc.show_text(text)

    def text_rect(self, gc, text):
        """ Return bounding rectangle for text, including margin. """
        with gc:
            gc.set_font(self.font)
            text_extent = gc.get_full_text_extent(text)
        width, height, descent, leading = text_extent

        x = -leading + self.margin
        y = self.margin
        width += 2 * self.margin
        height += 2 * self.margin - abs(descent)
        return x, y, width, height

    def bbox_offset(self, gc, text, width, height):
        """ Return offset distance for text rendering.

        If the origin is at the bottom-left, offsets are zero, and the margin
        is zero, then the returned offset values will be zero; otherwise, the
        returned offsets shift the text to account for these values.
        """
        x_bbox_offset = self._x_origin_factor * width + self.x_offset
        y_bbox_offset = self._y_origin_factor * height + self.y_offset
        return x_bbox_offset, y_bbox_offset

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _set_rotation_angle(self, gc, text, width, height):
        # Rotate label about center of bounding box
        gc.translate_ctm(width / 2.0, height / 2.0)
        gc.rotate_ctm(pi / 180.0 * self.rotate_angle)
        gc.translate_ctm(-width / 2.0, -height / 2.0)

    @cached_property
    def _get__x_origin_factor(self):
        # Fraction of label bounding-box width used to shift origin.
        if self.x_origin == 'center':
            return -0.5
        elif self.x_origin == 'left':
            return 0
        elif self.x_origin == 'right':
            return -1

    @cached_property
    def _get__y_origin_factor(self):
        # Fraction of label bounding-box height used to shift origin.
        if self.y_origin == 'center':
            return -0.5
        elif self.y_origin == 'top':
            return -1
        elif self.y_origin == 'bottom':
            return 0
