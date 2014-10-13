from __future__ import absolute_import

from pyface.qt import QtCore, QtGui, QtOpenGL

from vispy.gloo.context import GLContext
from vispy import gloo

from ..qt.utils import button_from_event


class QGLBackend(QtOpenGL.QGLWidget):
    """ OpenGL backend for WindowCanvas abstract class. """

    def __init__(self, parent, proxy_window):

        self._window = proxy_window
        self._window.control = self

        context = GLContext()
        context.take('qt', self)
        self._glcontext = context

        glformat = _set_config(context.config)

        window_flags = QtCore.Qt.Widget

        share_widget = None
        QtOpenGL.QGLWidget.__init__(self, glformat, parent,
                                    share_widget, window_flags)
        self.setAutoBufferSwap(False)
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setMouseTracking(True)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Expanding)

    def resizeEvent(self, event):
        size = event.size()
        self.resizeGL(size.width(), size.height())
        self._window.on_resize(event)

    def initializeGL(self):
        if self._window is None:
            return
        gloo.set_state(depth_test=False, blend=True, clear_color='white',
                       blend_func=('src_alpha', 'one_minus_src_alpha'))
        gloo.gl_initialize()

    def paintGL(self):
        if self._window is None:
            return
        if self.isValid():
            self._glcontext.set_current(False)  # Mark as current
            self.makeCurrent()
        self._window.render(None)

    def closeEvent(self, ev):
        self.close()
        self.doneCurrent()
        self.context().reset()

    def keyPressEvent(self, event):
        self._window.handle_key_event('key_press', event)

    def keyReleaseEvent(self, event):
        self._window.handle_key_event('key_release', event)

    def enterEvent(self, event):
        self._window.handle_mouse_event("mouse_enter", event)

    def leaveEvent(self, event):
        self._window.handle_mouse_event("mouse_leave", event)

    def mouseMoveEvent(self, event):
        self._window.handle_mouse_event("mouse_move", event)

    def mouseDoubleClickEvent(self, event):
        action_name = button_from_event(event) + '_dclick'
        self._window.handle_mouse_event(action_name, event)

    def mousePressEvent(self, event):
        action_name = button_from_event(event) + '_down'
        self._window.handle_mouse_event(action_name, event)

    def mouseReleaseEvent(self, event):
        action_name = button_from_event(event) + '_up'
        self._window.handle_mouse_event(action_name, event)

    def wheelEvent(self, event):
        self._window.handle_mouse_event("mouse_wheel", event)


    def sizeHint(self):
        qt_size_hint = super(QGLBackend, self).sizeHint()
        return self._window.get_size_hint(qt_size_hint)


def _set_config(c):
    """Set the OpenGL configuration from a gloo context."""
    glformat = QtOpenGL.QGLFormat()
    glformat.setRedBufferSize(c['red_size'])
    glformat.setGreenBufferSize(c['green_size'])
    glformat.setBlueBufferSize(c['blue_size'])
    glformat.setAlphaBufferSize(c['alpha_size'])
    glformat.setAccum(False)
    glformat.setRgba(True)
    glformat.setDoubleBuffer(True if c['double_buffer'] else False)
    glformat.setDepth(True if c['depth_size'] else False)
    glformat.setDepthBufferSize(c['depth_size'] if c['depth_size'] else 0)
    glformat.setStencil(True if c['stencil_size'] else False)
    glformat.setStencilBufferSize(c['stencil_size'] if c['stencil_size']
                                  else 0)
    glformat.setSampleBuffers(True if c['samples'] else False)
    glformat.setSamples(c['samples'] if c['samples'] else 0)
    glformat.setStereo(c['stereo'])
    return glformat
