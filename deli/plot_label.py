""" Defines the PlotLabel class.
"""
from traits.api import DelegatesTo, Enum, Instance, Str, Trait

from .abstract_overlay import AbstractOverlay
from .label import Label


LabelDelegate = DelegatesTo("_label")

class PlotLabel(AbstractOverlay):
    """ A label used by plots.

    This class wraps a simple Label instance, and delegates some traits to it.
    """

    # The text of the label.
    text = LabelDelegate
    # The color of the label text.
    color = DelegatesTo("_label")
    # The font for the label text.
    font = LabelDelegate
    # The angle of rotation of the label.
    angle = DelegatesTo("_label", "rotate_angle")

    #------------------------------------------------------------------------
    # Layout-related traits
    #------------------------------------------------------------------------

    hjustify = Enum("center", "left", "right")

    vjustify = Enum("center", "bottom", "top")

    overlay_position = Trait("outside top", Str, None)

    draw_layer = "plot"

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    # The label has a fixed height and can be resized horizontally.
    resizable = "h"

    # The Label instance this plot label is wrapping.
    _label = Instance(Label, args=())

    def __init__(self, text="", *args, **kw):
        super(PlotLabel, self).__init__(*args, **kw)
        self.text = text

    def overlay(self, component, gc, view_bounds=None, mode="normal"):
        """ Draws this label overlaid on another component.

        Overrides AbstractOverlay.
        """
        self._draw_overlay(gc, view_bounds, mode)

    def do_layout(self):
        """ Tells this component to do layout.

        Overrides PlotComponent.
        """
        self._layout_as_overlay()

    def _draw_overlay(self, gc, view_bounds=None, mode="normal"):
        """ Draws the overlay layer of a component.

        Overrides PlotComponent.
        """
        # Perform justification and compute the correct offsets for
        # the label position
        width, height = self._label.get_size(gc, self.text)

        x_offset = int((self.width - width) / 2)
        y_offset = int((self.height - height) / 2)

        with gc:
            # We have to translate to our position because the label
            # tries to draw at (0,0).
            gc.translate_ctm(self.x + x_offset, self.y + y_offset)
            self._label.draw(gc, self.text)

        return

    def _layout_as_overlay(self, size=None, force=False):
        """ Lays out the label as an overlay on another component.
        """
        if self.component is not None:
            orientation = self.overlay_position
            tmp = orientation.split()
            orientation = tmp[0]

            self.x = self.component.x
            self.width = self.component.width
            self.y = self.component.y2 + 1
            self.height = self.component.padding_top

    def _text_changed(self, old, new):
        self._label.text = new
        self.do_layout()

    def _font_changed(self, old, new):
        self._label.font = new
        self.do_layout()

    def _overlay_position_changed(self):
        self.do_layout()

    def _component_changed(self, old, new):
        self.draw_layer = "overlay"
