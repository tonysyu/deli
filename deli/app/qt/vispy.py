from __future__ import absolute_import

from traits.api import Instance

from ..vispy.graphics_context import GraphicsContext
from ..vispy.qgl_backend import QGLBackend
from .base_window import BaseWindow


class Window(BaseWindow):

    _gc = Instance(GraphicsContext)

    control = Instance(QGLBackend)

    def _create_control(self, parent, proxy_window):
        """ Create the toolkit control. """
        return QGLBackend(parent, proxy_window)

    def _create_gc(self, size, pix_format="bgra32"):
        self._gc = GraphicsContext(size)
        return self._gc

    def _render(self, event):
        if self.control is None:
            return

        self._gc.render(event)
        self.control.swapBuffers()
