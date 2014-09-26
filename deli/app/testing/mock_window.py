from mock import MagicMock

from enable.events import KeyEvent, MouseEvent
from traits.api import ABCHasStrictTraits, Any, Instance, Int, Tuple

from deli.testing.helpers import Bunch
from deli.utils.drawing import broadcast_points
from ..abstract_window import AbstractWindow


WIDTH = 700
HEIGHT = 500


def calculate_text_extent(text):
    width = len(text)
    height = 1
    leading = descent = 0
    return width, height, descent, leading


class MockContext(MagicMock):

    def __exit__(self, *args):
        pass


class MockKeyEvent(Bunch):

    def __init__(self, **kwargs):
        kwargs.setdefault('x', 0)
        kwargs.setdefault('y', 0)
        kwargs.setdefault('alt_down', False)
        kwargs.setdefault('control_down', False)
        kwargs.setdefault('shift_down', False)
        super(MockKeyEvent, self).__init__(**kwargs)


class MockControl(ABCHasStrictTraits):

    width = Int(WIDTH)
    height = Int(HEIGHT)

    handler = Any

    def __init__(self, mock_window):
        self.handler = mock_window

    def close(self):
        self.handler.on_close(None)
        self.handler = None

    def render(self):
        self.handler.render(None)

    def resize(self, new_size):
        self.handler.on_resize(new_size)

    def press_key(self, **kwargs):
        self.handler.handle_key_event('key_press', MockKeyEvent(**kwargs))

    def release_key(self, **kwargs):
        self.handler.handle_key_event('key_release', MockKeyEvent(**kwargs))

    def press_release_key(self, **kwargs):
        self.press_key(**kwargs)
        self.release_key(**kwargs)

    def fire_enter_event(self, **kwargs):
        self.handler.handle_mouse_event("mouse_enter", Bunch(**kwargs))

    def fire_leave_event(self, **kwargs):
        self.handler.handle_mouse_event("mouse_leave", Bunch(**kwargs))

    def move_mouse(self, **kwargs):
        self.handler.handle_mouse_event("mouse_move", Bunch(**kwargs))

    def double_click_mouse(self, button='left', **kwargs):
        action_name = '{}_dclick'.format(button)
        self.handler.handle_mouse_event(action_name, Bunch(**kwargs))

    def press_mouse_button(self, button='left', **kwargs):
        action_name = '{}_down'.format(button)
        self.handler.handle_mouse_event(action_name, Bunch(**kwargs))

    def release_mouse_button(self, button='left', **kwargs):
        action_name = '{}_up'.format(button)
        self.handler.handle_mouse_event(action_name, Bunch(**kwargs))

    def scroll_mouse_wheel(self, **kwargs):
        self.handler.handle_mouse_event("mouse_wheel", Bunch(**kwargs))

    def press_move_release(self, x, y, button='left'):
        points = broadcast_points(x, y)
        assert len(points) in (2, 3)

        pt_press, pt_move = points[:2]
        pt_release = pt_move if len(points) == 2 else points[2]
        to_kwargs = lambda pt: {'x': pt[0], 'y': pt[1]}

        self.press_mouse_button(button=button, **to_kwargs(pt_press))
        self.move_mouse(button=button, **to_kwargs(pt_move))
        self.release_mouse_button(button=button, **to_kwargs(pt_release))


class MockWindow(AbstractWindow):

    control = Instance(MockControl)
    _last_mouse_position = Tuple((0, 0))

    # -----------------------------------------------------------------------
    #  AbstractWindow interface
    # -----------------------------------------------------------------------

    def _control_default(self):
        return MockControl(self)

    def _render(self, event):
        pass

    def _create_gc(self, size):
        context = MagicMock()
        context.get_full_text_extent.side_effect = calculate_text_extent
        return context

    def _create_key_event(self, event_type, event):
        if self.component is None:
            return None

        if not event.character:
            return None
        return KeyEvent(window=self, event_type=event_type, **event.to_dict())

    def _create_mouse_event(self, event):
        # If the control no longer exists, don't send mouse event
        if self.control is None:
            return None
        self._last_mouse_position = (event.x, event.y)
        return MouseEvent(window=self, **event.to_dict())

    def redraw(self, rect=None):
        self.render()

    def _get_control_size(self):
        if self.control:
            return (self.control.width, self.control.height)
        return None

    def set_pointer(self, pointer):
        pass

    def set_tooltip(self, tooltip):
        pass

    def _set_focus(self):
        pass

    def _get_event_size(self, event):
        """ Return width and height of event. """
        size = event.size()
        return size.width(), size.height()
