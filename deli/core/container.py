""" Defines the basic Container class """
from contextlib import contextmanager

from enable.base import empty_rectangle, intersect_bounds
from enable.events import MouseEvent
from kiva import affine
from traits.api import Bool, Instance, List, Property, Tuple

from .component import Component


class Container(Component):
    """ A Container that holds other Components (or containers).

    If auto_size is True, the container will automatically update its bounds to
    enclose all of the components handed to it, so that a container's bounds
    serve as a bounding box (although not necessarily a minimal bounding box)
    of its contained components.
    """

    # The list of components within this frame
    components = Property    # List(Component)

    # Whether or not the container should auto-size itself to fit all of its
    # components.
    auto_size = Bool(False)

    # The layers that the container will draw first, so that they appear
    # under the component layers of the same name.
    container_under_layers = Tuple('background', 'underlay')

    # The layers that the container will draw last, so that they appear
    # over the component layers of the same name.
    container_over_layers = Tuple('overlay', 'border')

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    # Shadow trait for self.components
    _components = List    # List(Component)

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

    #------------------------------------------------------------------------
    # Protected methods
    #------------------------------------------------------------------------

    def draw_layer(self, layer, gc, view_bounds):
        """ Renders the named *layer* of this component.
        """
        new_bounds = self._local_bounds(view_bounds)
        if new_bounds == empty_rectangle:
            return

        if self.layout_needed:
            self.do_layout()

        # Give the container a chance to draw first for the layers that are
        # considered "under" or "at" the main layer level
        if layer in self.container_under_layers:
            self._draw_container_layer(layer, gc, view_bounds)

        self._draw_children(layer, gc, view_bounds)

        if layer in self.container_over_layers:
            self._draw_container_layer(layer, gc, view_bounds)

    def _draw_children(self, layer, gc, view_bounds):
        # Draw children with coordinates relative to container.
        visible_components = self._get_visible_components(view_bounds)
        if visible_components:
            with gc:
                gc.translate_ctm(*self.position)
                for component in visible_components:
                    component.draw_layer(layer, gc, view_bounds)

    def _draw_container_layer(self, layer, gc, view_bounds):
            draw = getattr(self, '_draw_container_' + layer, None)
            if draw:
                draw(gc, view_bounds)

    def _draw_container_background(self, gc, view_bounds=None):
        self._draw_background(gc, view_bounds)

    def _draw_container_overlay(self, gc, view_bounds=None):
        self._draw_overlay(gc, view_bounds)

    def _draw_container_underlay(self, gc, view_bounds=None):
        self._draw_underlay(gc, view_bounds)

    def _draw_container_border(self, gc, view_bounds=None):
        self._draw_border(gc, view_bounds)

    def _get_visible_components(self, bounds):
        """ Returns a list of this plot's children that are in the bounds. """
        if bounds is None:
            return [c for c in self.components if c.visible]

        visible_components = []
        for component in self.components:
            if not component.visible:
                continue
            tmp = intersect_bounds(component.outer_position +
                                   component.outer_bounds, bounds)
            if tmp != empty_rectangle:
                visible_components.append(component)
        return visible_components

    def _should_layout(self, component):
        """ Returns True if it is appropriate for the container to lay out
        the component; False if not.
        """
        if not component or \
            (not component.visible and not component.invisible_layout):
            return False
        else:
            return True

    def _local_bounds(self, view_bounds):
        """ Return bounds transformed to local space. """
        # Check if we are visible
        tmp = intersect_bounds(self.position + self.bounds, view_bounds)
        if tmp == empty_rectangle:
            return empty_rectangle
        # Compute new_bounds, which is the view_bounds transformed into
        # our coordinate space
        x, y, width, height = view_bounds
        new_bounds = (x-self.x, y-self.y, width, height)
        return new_bounds

    def _component_bounds_changed(self, component):
        "Called by contained objects when their bounds change"
        pass

    #------------------------------------------------------------------------
    # Property setters & getters
    #------------------------------------------------------------------------

    def _get_components(self):
        return self._components

    def _get_layout_needed(self):
        # Override the parent implementation to take into account whether any
        # of our contained components need layout.
        if self._layout_needed:
            return True
        else:
            for c in self.components:
                if c.layout_needed:
                    return True
            else:
                return False

    #------------------------------------------------------------------------
    # Event handling
    #------------------------------------------------------------------------

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
            # Dispatch event and add event handlers to the list of previous
            # event handlers if they actually receive the event.
            self._prev_event_handlers = set()
            for component in components:
                component.dispatch(event, suffix)
                self._prev_event_handlers.add(component)
                if event.handled:
                    break

        if not event.handled:
            super(Container, self).dispatch(event, suffix)

    @contextmanager
    def _local_event_transform(self, event):
        # Translate the event's location to be relative to this container.
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

    #------------------------------------------------------------------------
    # Event handlers
    #------------------------------------------------------------------------

    def _bounds_changed(self, old, new):
        # crappy... calling our parent's handler seems like a common traits
        # event handling problem
        super(Container, self)._bounds_changed(old, new)
        self._layout_needed = True

    def __components_items_changed(self, event):
        self._layout_needed = True
