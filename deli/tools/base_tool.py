"""
Defines the base class for all Chaco tools.  See docs/event_handling.txt for an
overview of how event handling works in Chaco.
"""
from enable.component import Component
from traits.api import HasStrictTraits, Instance, Str


class BaseTool(HasStrictTraits):
    """ The base class for Deli tools. """

    # The component that this tool is attached to.
    component = Instance(Component)


class BaseHandlerMethodTool(BaseTool):
    """ The base class for Deli tools. """

    # Name of the object's event state.  Used as a prefix when looking up
    # which set of event handlers should be used for MouseEvents and KeyEvents.
    # Subclasses should override this with an enumeration of their possible
    # states.
    event_state = Str("normal")

    def dispatch(self, event, suffix):
        """ Dispatch interactive event to the appropriate handler method. """
        handler = getattr(self, self.event_state + "_" + suffix, None)
        if handler is not None:
            handler(event)
