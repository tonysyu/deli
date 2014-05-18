""" Defines the basic Container class """
import warnings

from enable.base import empty_rectangle, intersect_bounds
from enable.events import MouseEvent
from kiva import affine
from traits.api import Bool, HasStrictTraits, Instance, List, Property, Tuple

from .component import Component


class AbstractResolver(HasStrictTraits):
    """
    A Resolver traverses a component DB and matches a specifier.
    """

    def match(self, db, query):
        """ Queries a component DB using a dict of keyword-val conditions.
        Each resolver defines its set of allowed keywords.
        """
        raise NotImplementedError


class Container(Component):
    """
    A Container is a logical container that holds other Components within it and
    provides an origin for Components to position themselves.  Containers can
    be "nested" (although "overlayed" is probably a better term).

    If auto_size is True, the container will automatically update its bounds to
    enclose all of the components handed to it, so that a container's bounds
    serve as abounding box (although not necessarily a minimal bounding box) of
    its contained components.
    """

    # The list of components within this frame
    components = Property    # List(Component)

    # If true, the container get events before its children.  Otherwise, it
    # gets them afterwards.
    intercept_events = Bool(True)

    # Whether or not the container should auto-size itself to fit all of its
    # components.
    auto_size = Bool(False)

    # The default size of this container if it is empty.
    default_size = Tuple(0, 0)

    # The layers that the container will draw first, so that they appear
    # under the component layers of the same name.
    container_under_layers = Tuple('background', 'underlay')

    # The layers that the container will draw last, so that they appear
    # over the component layers of the same name.
    container_over_layers = Tuple('overlay', 'border')

    #------------------------------------------------------------------------
    # DOM-related traits
    # (Note: These are unused as of 8/13/2007)
    #------------------------------------------------------------------------

    # This object resolves queries for components
    resolver = Instance(AbstractResolver)

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    # Shadow trait for self.components
    _components = List    # List(Component)

    # Set of components that last handled a mouse event.  We keep track of
    # this so that we can generate mouse_enter and mouse_leave events of
    # our own.
    _prev_event_handlers = Instance(set, ())

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def __init__(self, *components, **traits):
        Component.__init__(self, **traits)
        for component in components:
            self.add(component)
        if 'bounds' in traits.keys() and 'auto_size' not in traits.keys():
            self.auto_size = False

        if 'intercept_events' in traits:
            warnings.warn("'intercept_events' is a deprecated trait",
                    warnings.DeprecationWarning)
        return

    def add(self, *components):
        """ Adds components to this container """
        for component in components:
            if component.container is not None:
                component.container.remove(component)
            component.container = self
        self._components.extend(components)

    def components_at(self, x, y):
        """
        Returns a list of the components underneath the given point (given in
        the parent coordinate frame of this container).
        """
        result = []
        if self.is_in(x,y):
            xprime = x - self.position[0]
            yprime = y - self.position[1]
            for component in self._components[::-1]:
                if component.is_in(xprime, yprime):
                    result.append(component)
        return result

    def get(self, **kw):
        """
        Allows for querying of this container's components.
        """
        # TODO: cache requests
        return self.resolver.query(self._components, kw)

    def cleanup(self, window):
        """When a window viewing or containing a component is destroyed,
        cleanup is called on the component to give it the opportunity to
        delete any transient state it may have (such as backbuffers)."""
        if self._components:
            for component in self._components:
                component.cleanup(window)

    #------------------------------------------------------------------------
    # Protected methods
    #------------------------------------------------------------------------

    def _dispatch_draw(self, layer, gc, view_bounds):
        """ Renders the named *layer* of this component.
        """
        new_bounds = self._transform_view_bounds(view_bounds)
        if new_bounds == empty_rectangle:
            return

        if self.layout_needed:
            self.do_layout()

        # Give the container a chance to draw first for the layers that are
        # considered "under" or "at" the main layer level
        if layer in self.container_under_layers:
            self._draw_container_layer(layer, gc, view_bounds)

        # Now transform coordinates and draw the children
        visible_components = self._get_visible_components(new_bounds)
        if visible_components:
            with gc:
                gc.translate_ctm(*self.position)
                for component in visible_components:
                    component._dispatch_draw(layer, gc, new_bounds)

        if layer in self.container_over_layers:
            self._draw_container_layer(layer, gc, view_bounds)

    def _draw_container_layer(self, layer, gc, view_bounds):
            draw = getattr(self, '_draw_container_' + layer, None)
            if draw:
                draw(gc, view_bounds)

    def _draw_container(self, gc):
        "Draw the container background in a specified graphics context"
        pass

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

    def _transform_view_bounds(self, view_bounds):
        """
        Transforms the given view bounds into our local space and computes a new
        region that can be handed off to our children.  Returns a 4-tuple of
        the new position+bounds, or None (if None was passed in), or the value
        of empty_rectangle (from enable.base) if the intersection resulted
        in a null region.
        """
        # Check if we are visible
        tmp = intersect_bounds(self.position + self.bounds, view_bounds)
        if tmp == empty_rectangle:
            return empty_rectangle
        # Compute new_bounds, which is the view_bounds transformed into
        # our coordinate space
        v = view_bounds
        new_bounds = (v[0]-self.x, v[1]-self.y, v[2], v[3])
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

    def get_event_transform(self, event=None, suffix=""):
        return affine.affine_from_translation(-self.x, -self.y)

    def dispatch(self, event, suffix):
        """
        Dispatches a mouse event based on the current event_state.  Overrides
        the default Interactor.dispatch by adding some default
        behavior to send all events to our contained children.

        "suffix" is the name of the mouse event as a suffix to the event state
        name, e.g. "_left_down" or "_window_enter".
        """
        if not event.handled:
            components = self.components_at(event.x, event.y)

            # Translate the event's location to be relative to this container
            transform = self.get_event_transform(event, suffix)
            event.push_transform(transform, caller=self)

            try:
                component_set = set(components)

                # For 'real' mouse events (i.e., not pre_mouse_* events),
                # notify the previous listening components of a mouse leave
                if not suffix.startswith('pre_'):
                    components_left = self._prev_event_handlers - component_set
                    self._notify_if_mouse_event(components_left, event,
                                                'mouse_leave')

                    if suffix != 'mouse_leave':
                        components_entered = (component_set
                                              - self._prev_event_handlers)
                        self._notify_if_mouse_event(components_entered, event,
                                                    'mouse_enter')
                # Handle the actual event
                # Only add event handlers to the list of previous event handlers
                # if they actually receive the event (and the event is not a
                # pre_* event.
                if not suffix.startswith('pre_'):
                    self._prev_event_handlers = set()
                for component in components:
                    component.dispatch(event, suffix)
                    if not suffix.startswith('pre_'):
                        self._prev_event_handlers.add(component)
                    if event.handled:
                        break
            finally:
                event.pop(caller=self)

            if not event.handled:
                super(Container, self).dispatch(event, suffix)

    def _notify_if_mouse_event(self, components, event, suffix):
        if len(components) == 0:
            return

        if isinstance(event, MouseEvent):
            for component in components:
                component.dispatch(event, 'pre_' + suffix)
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
