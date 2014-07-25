from traits.api import Any, Bool

from ..abstract_window import AbstractWindow
from .graphics_context import GraphicsContext
from ._server import serve_and_open


class Painter(object):

    def __init__(self, control):
        self.control = control

    def draw_image(self, rect, image):
        serve_and_open("<h1> Hi </hi")


class Window(AbstractWindow):

    control = Any
    in_paint_event = Bool

    def _create_gc(self, size, pix_format="bgra32"):
        gc_size = (size[0]+1, size[1]+1)
        # We have to set bottom_up=0 or otherwise the PixelMap will appear
        # upside down in the QImage.
        gc = GraphicsContext(gc_size, pix_format=pix_format, bottom_up=0)
        gc.translate_ctm(0.5, 0.5)
        return gc

    def paintEvent(self, event):
        self.in_paint_event = True
        self._paint(event)
        self.in_paint_event = False

    def _get_control_size(self):
        if self.control:
            return (self.control.width(), self.control.height())
        else:
            return (400, 400)

    def _window_paint(self, event):
        w = self._gc.width()
        h = self._gc.height()
        rect = (0, 0, w, h)
        painter = Painter(self.control)
        image = None
        painter.draw_image(rect, image)

    def _redraw(self):
        pass

    def show(self):
        self.paintEvent(None)
