from pyface.qt import QtCore, QtGui


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
        self.handler.on_paint(event)

    def resizeEvent(self, event):
        self.handler.on_resize(event)

    def keyPressEvent(self, event):
        self.handler.on_key_press(event)

    def keyReleaseEvent(self, event):
        self.handler.on_key_release(event)

    def enterEvent(self, event):
        self.handler.on_mouse_enter(event)

    def leaveEvent(self, event):
        self.handler.on_mouse_leave(event)

    def mouseDoubleClickEvent(self, event):
        self.handler.on_mouse_double_click(event)

    def mouseMoveEvent(self, event):
        self.handler.on_mouse_move(event)

    def mousePressEvent(self, event):
        self.handler.on_mouse_press(event)

    def mouseReleaseEvent(self, event):
        self.handler.on_mouse_release(event)

    def wheelEvent(self, event):
        self.handler.on_mouse_wheel(event)

    def sizeHint(self):
        qt_size_hint = super(QtWindow, self).sizeHint()
        return self.handler.get_size_hint(qt_size_hint)
