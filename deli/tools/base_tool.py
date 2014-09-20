"""
Base classes for tools and tool-states.

Tools and tool-states can define any of the following methods to handle events
of interest:

- on_left_down
- on_left_up
- on_left_dclick
- on_right_down
- on_right_up
- on_right_dclick
- on_middle_down
- on_middle_up
- on_middle_dclick
- on_mouse_move
- on_mouse_wheel
- on_mouse_enter
- on_mouse_leave
- on_key_press
- on_key_release

"""
from traits.api import Dict, HasStrictTraits, Instance, Str, WeakRef

from ..core.component import Component


NULL_HANDLER = lambda x: None


class AbstractTool(HasStrictTraits):
    """ The base class for Deli tools. """

    # The component that this tool is attached to.
    component = Instance(Component)


class BaseToolState(AbstractTool):
    """ Base class for State objects that handle events while a tool is in
    a given state.

    This tool-state can define any methods to handle any event of interest.
    See module docstring for details.

    If an event triggers the state to exit, this object should call its
    `exit_state` method and, optionally, set the new state of the parent tool.
    """

    # The parent tool for this tool-state object.
    parent = WeakRef(AbstractTool)

    def __init__(self, parent, **kwtraits):
        super(BaseToolState, self).__init__(**kwtraits)
        self.parent = parent
        self.component = parent.component

    def on_enter(self, event):
        pass

    def exit_state(self, event, new_state=None):
        self.parent.state_change(event, new_state=new_state)
        self.on_exit(event, new_state=new_state)

    def on_exit(self, event, new_state=None):
        pass

    def on_mouse_leave(self, event):
        # Typically we want to exit to the normal state when leaving.
        self.exit_state(event)


class BaseTool(AbstractTool):
    """ Base class for tools

    Different event states are delegated to state-objects which handle events.

    Subclasses should define a dictionary of `state_handlers`, which maps
    state-names to `BaseToolState` objects that handle events. If the
    `active_handler` is set to `None`, then this tool will handle events
    directly.
    """

    state_handlers = Dict(Str, BaseToolState)

    active_handler = Instance(AbstractTool)

    @classmethod
    def attach_to(cls, component):
        instance = cls(component=component)
        component.tools.append(instance)

        overlay = getattr(instance, 'overlay', None)
        if overlay is not None:
            component.overlays.append(overlay)

        return instance

    def dispatch(self, event, suffix):
        """ Dispatch interactive event to the appropriate handler method.

        Parameters
        ----------
        event : BaseEvent instance
            The event to dispatch
        suffix : string
            The type of event that occurred.  See class docstring for the
            list of possible suffixes.
        """
        if self.active_handler is None:
            self.active_handler = self
            self.active_handler.on_enter(event)

        handler = getattr(self.active_handler, 'on_' + suffix, NULL_HANDLER)
        handler(event)

    def state_change(self, event, new_state=None):
        """ React to an event that changes the tool's state.

        The active handler will be updated in response to the state change.
        """
        if new_state is None:
            self.active_handler = self
        else:
            self.active_handler = self.state_handlers[new_state]
        self.active_handler.on_enter(event)

    def on_enter(self, event):
        pass
