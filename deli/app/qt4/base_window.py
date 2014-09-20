from pyface.qt import QtGui

from enable.events import KeyEvent, MouseEvent
from traits.api import Instance, Tuple

from ..abstract_window import AbstractWindow
from .constants import POINTER_MAP
from .qt_window import QtWindow
from .utils import get_button_state, get_modifier_state, key_from_event


class BaseWindow(AbstractWindow):

    control = Instance(QtGui.QWidget)
    _last_mouse_position = Tuple

    def __init__(self, parent, wid=-1, pos=None, size=None, **traits):
        super(AbstractWindow, self).__init__(**traits)

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
        return QtWindow(parent, enable_window)

    # -----------------------------------------------------------------------
    #  AbstractWindow interface
    # -----------------------------------------------------------------------

    def _create_key_event(self, event_type, event):
        if self.component is None:
            event.ignore()
            return None

        key = key_from_event(event_type, event)
        if not key:
            return None

        x, y = self._last_mouse_position
        y = self._flip_y(y)
        kwargs = get_modifier_state(event.modifiers())

        return KeyEvent(character=key, x=x, y=y, window=self, **kwargs)

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

        kwargs = get_modifier_state(modifiers)
        kwargs.update(get_button_state(buttons))
        return MouseEvent(x=x, y=self._flip_y(y), window=self, **kwargs)

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

    def set_pointer(self, pointer):
        self.control.setCursor(POINTER_MAP[pointer])

    def set_tooltip(self, tooltip):
        self.control.setToolTip(tooltip)

    def _set_focus(self):
        self.control.setFocus()

    def _get_event_size(self, event):
        """ Return width and height of event. """
        size = event.size()
        return size.width(), size.height()

    # -----------------------------------------------------------------------
    #  Private methods
    # -----------------------------------------------------------------------

    def _flip_y(self, y):
        "Converts between a Kiva and a Qt y coordinate"
        return int(self._size[1] - y - 1)

    def get_size_hint(self, qt_size_hint):
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
        preferred_size = self.component.get_preferred_size()
        q_size = self.control.size()
        window_size = (q_size.width(), q_size.height())

        if qt_size_hint.width() < 0:
            width = max(preferred_size[0], window_size[0])
            qt_size_hint.setWidth(width)

        if qt_size_hint.height() < 0:
            height = max(preferred_size[1], window_size[1])
            qt_size_hint.setHeight(height)

        return qt_size_hint
