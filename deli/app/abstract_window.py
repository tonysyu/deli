from enable.colors import ColorTrait
from traits.api import (Any, Bool, Event, HasStrictTraits, Instance, Property,
                        Trait, Tuple)

from ..core.component import Component
from ..core.container import Container


def Alias(name):
    return Property(lambda obj: getattr(obj, name),
                    lambda obj, val: setattr(obj, name, val))


class AbstractWindow(HasStrictTraits):

    # The top-level component that this window houses
    component = Instance(Component)

    # The background window of the window.  The entire window first gets
    # painted with this color before the component gets to draw.
    bgcolor = ColorTrait("sys_window")

    alt_pressed = Bool(False)
    control_pressed = Bool(False)
    shift_pressed = Bool(False)

    # When the underlying toolkit control gets resized, this event gets set
    # to the new size of the window, expressed as a tuple (dx, dy).
    resized = Event

    # Kiva GraphicsContext (XXX: is there a base class?)
    _gc = Any

    # The previous component that handled an event.  Used to generate
    # mouse_enter and mouse_leave events.  Right now this can only be
    # None, self.component, or self.overlay.
    _prev_event_handler = Instance(Component)

    # Integer size of the Window (width, height).
    _size = Trait(None, Tuple)

    # --------------------------------------------------------------------------
    #  Abstract methods that must be implemented by concrete subclasses
    # --------------------------------------------------------------------------

    def _create_key_event(self, event):
        "Convert a GUI toolkit key event into a KeyEvent"
        raise NotImplementedError()

    def _create_mouse_event(self, event):
        "Convert a GUI toolkit mouse event into a MouseEvent"
        raise NotImplementedError()

    def _get_control_size(self):
        "Get the size of the underlying toolkit control"
        raise NotImplementedError()

    def _create_gc(self, size, pix_format="bgr24"):
        """ Create a Kiva graphics context of a specified size.  This method
        only gets called when the size of the window itself has changed.  To
        perform pre-draw initialization every time in the paint loop, use
        _init_gc().
        """
        raise NotImplementedError()

    def _init_gc(self):
        """ Gives a GC a chance to initialize itself before components perform
        layout and draw.  This is called every time through the paint loop.
        """
        gc = self._gc
        gc.clear(self.bgcolor_)

    def _window_paint(self, event):
        "Do a GUI toolkit specific screen update"
        raise NotImplementedError()

    def set_pointer(self, pointer):
        "Sets the current cursor shape"
        raise NotImplementedError()

    def _set_focus(self):
        "Sets this window to have keyboard focus"
        raise NotImplementedError()

    # -----------------------------------------------------------------------
    # Public methods
    # -----------------------------------------------------------------------

    def __init__(self, **traits):
        self._gc = None
        super(HasStrictTraits, self).__init__(**traits)

        # Create a default component (if necessary):
        if self.component is None:
            self.component = Container()

    def _component_changed(self, old, new):
        if old is not None:
            old.window = None

        if new is None:
            self.component = Container()
            return

        new.window = self

        # If possible, size the new component according to the size of the
        # toolkit control
        size = self._get_control_size()
        if (size is not None) and hasattr(self.component, "size"):
            self.component.origin = [0, 0]
            self.component.size = list(size)
        self.redraw()

    # --------------------------------------------------------------------------
    #  Generic keyboard event handler:
    # --------------------------------------------------------------------------

    def _handle_key_event(self, event_type, event):
        """ **event** should be a toolkit-specific opaque object that will
        be passed in to the backend's _create_key_event() method. It can
        be None if the the toolkit lacks a native "key event" object.

        Returns True if the event has been handled within the Enable object
        hierarchy, or False otherwise.
        """
        # Generate the Enable event
        key_event = self._create_key_event(event_type, event)
        if key_event is None:
            return False

        self.alt_pressed = key_event.alt_down
        self.control_pressed = key_event.control_down
        self.shift_pressed = key_event.shift_down

        # Normal event handling loop
        if (not key_event.handled) and (self.component is not None):
            if self.component.is_in(key_event.x, key_event.y):
                # Fire the actual event
                self.component.dispatch(key_event, event_type)

        return key_event.handled

    # --------------------------------------------------------------------------
    #  Generic mouse event handler:
    # --------------------------------------------------------------------------

    def handle_mouse_event(self, event_name, event, set_focus=False):
        """ **event** should be a toolkit-specific opaque object that will
        be passed in to the backend's _create_mouse_event() method.  It can
        be None if the the toolkit lacks a native "mouse event" object.

        Returns True if the event has been handled within the Enable object
        hierarchy, or False otherwise.
        """
        if self._size is None:
            return False

        mouse_event = self._create_mouse_event(event)
        xy = (mouse_event.x, mouse_event.y)

        if (not mouse_event.handled) and (self.component is not None):
            # Test to see if we need to generate a mouse_leave event
            if self._prev_event_handler:
                if not self._prev_event_handler.is_in(*xy):
                    mouse_event.handled = False
                    self._prev_event_handler.dispatch(mouse_event,
                                                      "mouse_leave")
                    self._prev_event_handler = None

            if self.component.is_in(*xy):
                # Test to see if we need to generate a mouse_enter event
                if self._prev_event_handler != self.component:
                    self._prev_event_handler = self.component
                    mouse_event.handled = False
                    self.component.dispatch(mouse_event, "mouse_enter")

                # Fire the actual event
                mouse_event.handled = False
                self.component.dispatch(mouse_event, event_name)
        return mouse_event.handled

    def redraw(self, rect=None):
        """ Request a redraw of the window

        If `rect` is provided, draw within just the (x, y, w, h) rectangle.
        Otherwise, draw over the entire window.
        """
        raise NotImplementedError()

    def cleanup(self):
        """ Clean up after ourselves.
        """
        if self.component is not None:
            self.component.cleanup(self)
            self.component.window = None
            self.component = None

        self.control = None
        if self._gc is not None:
            self._gc.window = None
            self._gc = None

    def _paint(self, event=None):
        """ This method is called directly by the UI toolkit's callback
        mechanism on the paint event.
        """
        # Create a new GC if necessary
        size = self._get_control_size()
        if (self._size != tuple(size)) or (self._gc is None):
            self._size = tuple(size)
            self._gc = self._create_gc(size)

        # Always give the GC a chance to initialize
        self._init_gc()

        # Layout components and draw
        if hasattr(self.component, "do_layout"):
            self.component.do_layout()
        gc = self._gc
        self.component.render(gc, view_rect=(0, 0, size[0], size[1]))

        # Perform a paint of the GC to the window (only necessary on backends
        # that render to an off-screen buffer)
        self._window_paint(event)

    # --------------------------------------------------------------------------
    # Wire up the keyboard event handlers
    # --------------------------------------------------------------------------

    def on_key_pressed(self, event):
        self._handle_key_event('key_pressed', event)

    def on_key_released(self, event):
        self._handle_key_event('key_released', event)

    def on_character(self, event):
        self._handle_key_event('character', event)
