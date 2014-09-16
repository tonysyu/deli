""" Defines the PlotLabel class.
"""
from traits.api import DelegatesTo, Instance

from .abstract_overlay import AbstractOverlay
from .stylus.label_stylus import LabelStylus


LabelDelegate = DelegatesTo("_label")


class PlotLabel(AbstractOverlay):
    """ A label used by plots.

    This class wraps a simple LabelStylus, and delegates some traits to it.
    """

    #: The text of the label.
    text = LabelDelegate

    #: The font for the label text.
    font = LabelDelegate

    #: Visibility of label. Off by default, but turned on when text is set.
    visible = False

    # The Label instance this plot label is wrapping.
    _label = Instance(LabelStylus, {'x_origin': 'center',
                                    'y_origin': 'bottom',
                                    'y_offset': 20})

    def __init__(self, text="", *args, **kw):
        super(PlotLabel, self).__init__(*args, **kw)
        self.text = text

    def draw(self, gc, view_rect=None):
        """ Draws this label overlaid on another component.

        Overrides AbstractOverlay.
        """
        self._draw_overlay(gc, view_rect)

    def do_layout(self):
        """ Tells this component to do layout.

        Overrides Component.
        """
        self._layout_as_overlay()

    def _draw_overlay(self, gc, view_rect=None):
        """ Draws the overlay layer of a component.

        Overrides Component.
        """
        with gc:
            gc.translate_ctm(self.x, self.y)
            self._label.draw(gc, self.text)

    def _layout_as_overlay(self, size=None, force=False):
        """ Lays out the label as an overlay on another component.
        """
        if self.component is not None:
            self.x = (self.component.width / 2.0)
            self.y = self.component.height

    def _text_changed(self, old, new):
        self._label.text = new
        self.visible = (new is not None and len(new) > 0)
        self.do_layout()

    def _font_changed(self, old, new):
        self._label.font = new
        self.do_layout()
