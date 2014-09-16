""" Defines the basic Container class """
from contextlib import contextmanager

from enable.base import empty_rectangle, intersect_bounds
from enable.events import MouseEvent
from kiva import affine
from traits.api import Instance, List, Property

from .component import Component


class Container(Component):
    """ A Container that holds components and other containers.

    This represents a general container class of a composite structure [GoF]_.

    .. [GoF] Design Patterns: Elements of Reusable Object Oriented Software,
             Gamma et al., Addison-Wesley, 1996.
    """

    # The list of components within this frame
    components = Property    # List(Component)

    # Shadow trait for self.components
    _components = List(Component)

    # Set of components that last handled a mouse event. This allows us to
    # generate mouse_enter and mouse_leave events of our own.
    _prev_event_handlers = Instance(set, ())

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def add(self, *components):
        """ Adds components to this container """
        for component in components:
            if component.container is not None:
                component.container.remove(component)
            component.container = self
        self._components.extend(components)

    def components_at(self, x, y):
        """ Returns components underneath the given point.

        Input point is specified in parent container's coordinate space.
        """
        result = []
        if self.is_in(x,y):
            for component in self._components[::-1]:
                if component.is_in(x - self.x, y - self.y):
                    result.append(component)
        return result

    def cleanup(self, window):
        """ Perform any necessary cleanup. """
        if self._components:
            for component in self._components:
                component.cleanup(window)

    def get_event_transform(self, event=None):
        return affine.affine_from_translation(-self.x, -self.y)

    def dispatch(self, event, suffix):
        """ Dispatches mouse event to child components until it is handled.

        Parameters
        ----------
        event : BaseEvent
            A mouse or key event.
        suffix : string
            The name of the mouse event as a suffix to the event state name,
            e.g. "left_down" or "window_enter".
        """
        if event.handled:
            return

        # Get components under event and then transform to local coordinates.
        components = self.components_at(event.x, event.y)
        with self._local_event_transform(event):
            component_set = set(components)

            components_left = self._prev_event_handlers - component_set
            self._notify_if_mouse_event(components_left, event, 'mouse_leave')

            if suffix != 'mouse_leave':
                components_entered = component_set - self._prev_event_handlers
                self._notify_if_mouse_event(components_entered,
                                            event, 'mouse_enter')

            self._prev_event_handlers = set()
            for component in components:
                component.dispatch(event, suffix)
                # Only add handler if it actually received the event.
                self._prev_event_handlers.add(component)
                if event.handled:
                    break

        if not event.handled:
            super(Container, self).dispatch(event, suffix)

    def draw_layer(self, layer, gc, view_rect):
        """ Renders the named *layer* of this component.
        """
        if view_rect == empty_rectangle:
            return

        draw_layer_ = super(Container, self).draw_layer

        if layer in ('background', 'underlay'):
            draw_layer_(layer, gc, view_rect)

        if layer == 'plot':
            self._draw_children(layer, gc, view_rect)

        if layer == 'overlay':
            draw_layer_(layer, gc, view_rect)

    #------------------------------------------------------------------------
    # Property setters & getters
    #------------------------------------------------------------------------

    def _get_components(self):
        return self._components

    def _get_layout_needed(self):
        # Override the parent implementation child components.
        return (self._layout_needed
                or any(c.layout_needed for c in self.components))

    #------------------------------------------------------------------------
    # Event handlers
    #------------------------------------------------------------------------

    def _component_origin_changed(self):
        """Called by contained objects when their origins change"""
        self._origin_changed()

    def _component_size_changed(self):
        """Called by contained objects when their size change"""
        self._size_changed()

    def _size_changed(self):
        super(Container, self)._size_changed()
        self._layout_needed = True

    @contextmanager
    def _local_event_transform(self, event):
        """ Translate event location to be relative to this container. """
        try:
            transform = self.get_event_transform(event)
            event.push_transform(transform, caller=self)
            yield
        finally:
            event.pop(caller=self)

    def _notify_if_mouse_event(self, components, event, suffix):
        if len(components) == 0:
            return

        if isinstance(event, MouseEvent):
            for component in components:
                component.dispatch(event, suffix)
                event.handled = False

    def __components_items_changed(self, event):
        self._layout_needed = True

    #--------------------------------------------------------------------------
    # Private interface
    #--------------------------------------------------------------------------

    def _draw_children(self, layer, gc, view_rect):
        # Draw children with coordinates relative to container.
        children = self._get_visible_components(view_rect)
        self._draw_layers(gc, children, view_rect=view_rect)

    def _get_visible_components(self, bounds):
        """ Returns a list of this plot's children that are in the bounds. """
        if bounds is None:
            return [c for c in self.components if c.visible]

        return [c for c in self.components
                if intersect_bounds(c.rect, bounds) != empty_rectangle]
