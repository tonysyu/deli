""" Defines the PlotLabel class.
"""
from traits.api import DelegatesTo, Instance

from .abstract_overlay import AbstractOverlay
from .artist.label_artist import LabelArtist


LabelDelegate = DelegatesTo("_label")


class PlotLabel(AbstractOverlay):
    """ A label used by plots.

    This class wraps a simple LabelArtist, and delegates some traits to it.
    """

    # The text of the label.
    text = LabelDelegate

    # The font for the label text.
    font = LabelDelegate

    draw_layer = "plot"

    # The Label instance this plot label is wrapping.
    _label = Instance(LabelArtist, {'x_origin': 'center'})

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
        x_center = self.x + (self.width / 2.0)
        y_center = self.y + (self.height / 2.0)

        with gc:
            gc.translate_ctm(x_center, y_center)
            self._label.draw(gc, self.text)

    def _layout_as_overlay(self, size=None, force=False):
        """ Lays out the label as an overlay on another component.
        """
        if self.component is not None:
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

    def _component_changed(self, old, new):
        self.draw_layer = "overlay"
