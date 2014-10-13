from pyface.qt import QtCore, QtGui

from .utils import button_from_event


class QtWindow(QtGui.QWidget):
    """ The Qt widget that implements the control layer. """

    def __init__(self, parent, proxy_window):
        super(QtWindow, self).__init__(parent)
        self.setAcceptDrops(True)
        self._window = proxy_window

        self.setAutoFillBackground(True)
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setMouseTracking(True)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Expanding)

    def closeEvent(self, event):
        self._window.on_close(event)
        self._window = None
        return super(QtWindow, self).closeEvent(event)

    def paintEvent(self, event):
        self._window.render(event)

    def resizeEvent(self, event):
        self._window.on_resize(event)

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
        qt_size_hint = super(QtWindow, self).sizeHint()
        return self._window.get_size_hint(qt_size_hint)
