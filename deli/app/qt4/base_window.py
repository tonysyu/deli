from pyface.qt import QtCore, QtGui

from enable.events import KeyEvent, MouseEvent
from traits.api import Instance, Tuple

from ..abstract_window import AbstractWindow
from .constants import BUTTON_NAME_MAP, KEY_MAP, POINTER_MAP


class _QtWindowHandler(object):

    def __init__(self, qt_window, enable_window):
        self._enable_window = enable_window

        self.in_paint_event = False

        qt_window.setAutoFillBackground(True)
        qt_window.setFocusPolicy(QtCore.Qt.WheelFocus)
        qt_window.setMouseTracking(True)
        qt_window.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                QtGui.QSizePolicy.Expanding)

    def closeEvent(self, event):
        self._enable_window.cleanup()
        self._enable_window = None

    def paintEvent(self, event):
        self.in_paint_event = True
        self._enable_window._paint(event)
        self.in_paint_event = False

    def resizeEvent(self, event):
        dx = event.size().width()
        dy = event.size().height()
        component = self._enable_window.component

        self._enable_window.resized = (dx, dy)

        component.origin = [0, 0]
        component.size = [dx, dy]

    # -----------------------------------------------------------------------
    # Qt Keyboard event handlers
    # -----------------------------------------------------------------------

    def keyPressEvent(self, event):
        if self._enable_window:
            if not self._enable_window._on_key_pressed(event):
                self._enable_window._on_character(event)

    def keyReleaseEvent(self, event):
        if self._enable_window:
            self._enable_window._on_key_released(event)

    # -----------------------------------------------------------------------
    # Qt Mouse event handlers
    # -----------------------------------------------------------------------

    def enterEvent(self, event):
        if self._enable_window:
            self._enable_window.handle_mouse_event("mouse_enter", event)

    def leaveEvent(self, event):
        if self._enable_window:
            self._enable_window.handle_mouse_event("mouse_leave", event)

    def mouseDoubleClickEvent(self, event):
        if self._enable_window:
            name = BUTTON_NAME_MAP[event.button()]
            self._enable_window.handle_mouse_event(name + "_dclick", event)

    def mouseMoveEvent(self, event):
        if self._enable_window:
            self._enable_window.handle_mouse_event("mouse_move", event)

    def mousePressEvent(self, event):
        if self._enable_window:
            name = BUTTON_NAME_MAP[event.button()]
            self._enable_window.handle_mouse_event(name + "_down", event)

    def mouseReleaseEvent(self, event):
        if self._enable_window:
            name = BUTTON_NAME_MAP[event.button()]
            self._enable_window.handle_mouse_event(name + "_up", event)

    def wheelEvent(self, event):
        if self._enable_window:
            self._enable_window.handle_mouse_event("mouse_wheel", event)

    def sizeHint(self, qt_size_hint):
        """ Combine the Qt and enable size hints.

        Combine the size hint coming from the Qt component (usually -1, -1)
        with the preferred size of the enable component and the size
        of the enable window.

        The combined size hint is
        - the Qt size hint if larger than 0
        - the maximum of the plot's preferred size and the window size
          (component-wise)

        E.g., if
        qt size hint = (-1, -1)
        component preferred size = (500, 200)
        size of enable window = (400, 400)

        the final size hint will be (500, 400)
        """
        preferred_size = self._enable_window.component.get_preferred_size()
        q_size = self._enable_window.control.size()
        window_size = (q_size.width(), q_size.height())

        if qt_size_hint.width() < 0:
            width = max(preferred_size[0], window_size[0])
            qt_size_hint.setWidth(width)

        if qt_size_hint.height() < 0:
            height = max(preferred_size[1], window_size[1])
            qt_size_hint.setHeight(height)

        return qt_size_hint


class _QtWindow(QtGui.QWidget):
    """ The Qt widget that implements the control layer. """

    def __init__(self, parent, enable_window):
        super(_QtWindow, self).__init__(parent)
        self.setAcceptDrops(True)
        self.handler = _QtWindowHandler(self, enable_window)

    def closeEvent(self, event):
        self.handler.closeEvent(event)
        return super(_QtWindow, self).closeEvent(event)

    def paintEvent(self, event):
        self.handler.paintEvent(event)

    def resizeEvent(self, event):
        self.handler.resizeEvent(event)

    def keyPressEvent(self, event):
        self.handler.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.handler.keyReleaseEvent(event)

    def enterEvent(self, event):
        self.handler.enterEvent(event)

    def leaveEvent(self, event):
        self.handler.leaveEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.handler.mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        self.handler.mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.handler.mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.handler.mouseReleaseEvent(event)

    def wheelEvent(self, event):
        self.handler.wheelEvent(event)

    def sizeHint(self):
        qt_size_hint = super(_QtWindow, self).sizeHint()
        return self.handler.sizeHint(qt_size_hint)


class BaseWindow(AbstractWindow):

    control = Instance(QtGui.QWidget)
    _last_mouse_position = Tuple

    def __init__(self, parent, wid=-1, pos=None, size=None, **traits):
        AbstractWindow.__init__(self, **traits)

        if isinstance(parent, QtGui.QLayout):
            parent = parent.parentWidget()

        self.control = self._create_control(parent, self)

        point = self.control.mapFromGlobal(QtGui.QCursor.pos())
        self._last_mouse_position = (point.x(), point.y())

        if pos is not None:
            self.control.move(*pos)

        if size is not None:
            self.control.resize(*size)

    def _create_control(self, parent, enable_window):
        """ Create the toolkit control. """
        return _QtWindow(parent, enable_window)

    # -----------------------------------------------------------------------
    # Implementations of abstract methods in AbstractWindow
    # -----------------------------------------------------------------------

    def _create_key_event(self, event_type, event):
        if self.component is None:
            event.ignore()
            return None

        if event_type == 'character':
            key = unicode(event.text())
        else:
            # Convert the keypress to a standard enable key if possible,
            # otherwise to text.
            key_code = event.key()
            key = KEY_MAP.get(key_code)
            if key is None:
                key = unichr(key_code).lower()

        if not key:
            return None

        # Use the last-seen mouse position as the coordinates of this event.
        x, y = self._last_mouse_position

        modifiers = event.modifiers()

        return KeyEvent(
            event_type=event_type,
            character=key,
            x=x,
            y=self._flip_y(y),
            alt_down=bool(modifiers & QtCore.Qt.AltModifier),
            shift_down=bool(modifiers & QtCore.Qt.ShiftModifier),
            control_down=bool(modifiers & QtCore.Qt.ControlModifier),
            event=event,
            window=self
        )

    def _create_mouse_event(self, event):
        # If the control no longer exists, don't send mouse event
        if self.control is None:
            return None
        # If the event (if there is one) doesn't contain the mouse position,
        # modifiers and buttons then get sensible defaults.
        try:
            x = event.x()
            y = event.y()
            modifiers = event.modifiers()
            buttons = event.buttons()
        except AttributeError:
            pos = self.control.mapFromGlobal(QtGui.QCursor.pos())
            x = pos.x()
            y = pos.y()
            modifiers = 0
            buttons = 0

        self._last_mouse_position = (x, y)
        return MouseEvent(
            x=x,
            y=self._flip_y(y),
            alt_down=bool(modifiers & QtCore.Qt.AltModifier),
            shift_down=bool(modifiers & QtCore.Qt.ShiftModifier),
            control_down=bool(modifiers & QtCore.Qt.ControlModifier),
            left_down=bool(buttons & QtCore.Qt.LeftButton),
            middle_down=bool(buttons & QtCore.Qt.MidButton),
            right_down=bool(buttons & QtCore.Qt.RightButton),
            window=self
        )

    def redraw(self, rect=None):
        if self.control:
            if rect is None:
                self.control.update()
            else:
                self.control.update(*rect)

    def _get_control_size(self):
        if self.control:
            return (self.control.width(), self.control.height())

        return None

    def _create_gc(self, size, pix_format="bgra32"):
        raise NotImplementedError

    def _window_paint(self, event):
        raise NotImplementedError

    def set_pointer(self, pointer):
        self.control.setCursor(POINTER_MAP[pointer])

    def set_tooltip(self, tooltip):
        self.control.setToolTip(tooltip)

    def _set_focus(self):
        self.control.setFocus()

    def _on_key_pressed(self, event):
        return self._handle_key_event('key_pressed', event)

    # -----------------------------------------------------------------------
    # Private methods
    # -----------------------------------------------------------------------

    def _flip_y(self, y):
        "Converts between a Kiva and a Qt y coordinate"
        return int(self._size[1] - y - 1)
