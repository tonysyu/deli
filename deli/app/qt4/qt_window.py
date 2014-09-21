from pyface.qt import QtCore, QtGui

from .constants import BUTTON_NAME_MAP


def button_from_event(event):
    return BUTTON_NAME_MAP[event.button()]


class QtWindow(QtGui.QWidget):
    """ The Qt widget that implements the control layer. """

    def __init__(self, parent, enable_window):
        super(QtWindow, self).__init__(parent)
        self.setAcceptDrops(True)
        self.handler = enable_window

        self.setAutoFillBackground(True)
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setMouseTracking(True)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Expanding)

    def closeEvent(self, event):
        self.handler.on_close(event)
        self.handler = None
        return super(QtWindow, self).closeEvent(event)

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
        qt_size_hint = super(QtWindow, self).sizeHint()
        return self.handler.get_size_hint(qt_size_hint)
