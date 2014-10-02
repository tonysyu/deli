"""
Adapted from `vispy.app.backends._qt`
"""
from pyface.qt import QtCore, QtOpenGL

from .qt_window import button_from_event


def _set_config(c):
    """Set the OpenGL configuration"""
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


class CanvasBackend(QtOpenGL.QGLWidget):

    """Qt backend for Canvas abstract class."""

    # args are for BaseCanvasBackend, kwargs are for us.
    def __init__(self, *args, **kwargs):
        # Maybe to ensure that exactly all arguments are passed?
        resize, dec, fs, parent, context, \
            = self._process_backend_kwargs(kwargs)
        self._initialized = False

        # Deal with context
        if not context.istaken:
            widget = kwargs.pop('shareWidget', None) or self
            context.take('qt', widget)
            glformat = _set_config(context.config)
            if widget is self:
                widget = None  # QGLWidget does not accept self ;)
        elif context.istaken == 'qt':
            widget = context.backend_canvas
            glformat = QtOpenGL.QGLFormat.defaultFormat()
            if 'shareWidget' in kwargs:
                raise RuntimeError('Cannot use vispy to share context and '
                                   'use built-in shareWidget.')
        else:
            raise RuntimeError('Different backends cannot share a context.')

        f = QtCore.Qt.Widget if dec else QtCore.Qt.FramelessWindowHint

        # first arg can be glformat, or a gl context
        QtOpenGL.QGLWidget.__init__(self, glformat, parent, widget, f)
        self._initialized = True
        if not self.isValid():
            raise RuntimeError('context could not be created')
        self.setAutoBufferSwap(False)  # to make consistent with other backends
        self.setMouseTracking(True)

    def closeEvent(self, event):
        self.handler.on_close(event)
        self.handler = None
        return super(CanvasBackend, self).closeEvent(event)

    def paintEvent(self, event):
        self.handler.render(event)

    def resizeEvent(self, event):
        self.handler.on_resize(event)

    def keyPressEvent(self, event):
        self.handler.handle_key_event('key_press', event)

    def keyReleaseEvent(self, event):
        self.handler.handle_key_event('key_release', event)

    def enterEvent(self, event):
        self.handler.handle_mouse_event("mouse_enter", event)

    def leaveEvent(self, event):
        self.handler.handle_mouse_event("mouse_leave", event)

    def mouseMoveEvent(self, event):
        self.handler.handle_mouse_event("mouse_move", event)

    def mouseDoubleClickEvent(self, event):
        action_name = button_from_event(event) + '_dclick'
        self.handler.handle_mouse_event(action_name, event)

    def mousePressEvent(self, event):
        action_name = button_from_event(event) + '_down'
        self.handler.handle_mouse_event(action_name, event)

    def mouseReleaseEvent(self, event):
        action_name = button_from_event(event) + '_up'
        self.handler.handle_mouse_event(action_name, event)

    def wheelEvent(self, event):
        self.handler.handle_mouse_event("mouse_wheel", event)

    def sizeHint(self):
        qt_size_hint = super(CanvasBackend, self).sizeHint()
        return self.handler.get_size_hint(qt_size_hint)
