from __future__ import absolute_import

from pyface.qt import QtCore, QtOpenGL

from vispy.gloo.context import GLContext
from vispy import gloo


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
        self.setMouseTracking(True)

    def resizeEvent(self, event):
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

    def sizeHint(self):
        return self.size()


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
