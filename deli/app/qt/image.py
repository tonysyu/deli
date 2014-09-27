from kiva.agg import GraphicsContextSystem as GraphicsContext
from pyface.qt import QtCore, QtGui

from .base_window import BaseWindow


class Window(BaseWindow):

    def _create_gc(self, size, pix_format="bgra32"):
        gc_size = (size[0]+1, size[1]+1)
        # We have to set bottom_up=0 or otherwise the PixelMap will appear
        # upside down in the QImage.
        gc = GraphicsContext(gc_size, pix_format=pix_format, bottom_up=0)
        gc.translate_ctm(0.5, 0.5)
        return gc

    def _render(self, event):
        if self.control is None:
            return

        w = self._gc.width()
        h = self._gc.height()
        data = self._gc.pixel_map.convert_to_argb32string()

        image = QtGui.QImage(data, w, h, QtGui.QImage.Format_ARGB32)
        rect = QtCore.QRect(0, 0, w, h)

        painter = QtGui.QPainter(self.control)
        painter.drawImage(rect, image)
