""" Defines the Component class """
from itertools import chain

from enable.colors import ColorTrait
from kiva.constants import FILL
from traits.api import Any, Bool, Instance, List, Property, Str, WeakRef

from ..layout.bounding_box import BoundingBox
from .coordinate_box import CoordinateBox


DRAWING_ORDER = ['background', 'underlay', 'plot', 'overlay']


class NullDispatch(object):

    @staticmethod
    def dispatch(event, suffix):
        pass


class Component(CoordinateBox):
    """ Component is the base class for most objects.

    This represents a general component of a composite structure [GoF]_, but,
    by itself, is only a leaf-component. `Containers`, which subclass
    `Component`, compose components and other containers.

    Drawing order is controlled by `_draw_<layer>` methods, where <layers> are:

    1. 'background': Background image, shading
    2. 'underlay': Axes and grids
    3. 'plot': The main plot area itself
    4. 'overlay': Legends, selection regions, and other tool-drawn elements

    .. [GoF] Design Patterns: Elements of Reusable Object Oriented Software,
             Gamma et al., Addison-Wesley, 1996.
    """

    # The element ID of this component.
    id = Str

    # Name of the class or protocol for this component. Defaults to class name.
    label = Str

    #------------------------------------------------------------------------
    # Components and containers
    #------------------------------------------------------------------------

    # The parent container for this component.
    container = WeakRef(CoordinateBox)

    # The top-level Window.
    window = Property   # Instance("Window")

    # Only gets set if this is the top-level enable component in a Window.
    _window = Any    # Instance("Window")

    # A list of underlays for this plot.
    underlays = List  #[AbstractOverlay]

    # A list of overlays for the plot.
    overlays = List   #[AbstractOverlay]

    # The tools that are registered as listeners.
    tools = List

    # The order in which various rendering classes on this component are drawn.
    draw_order = Instance(list, args=(DRAWING_ORDER,))

    #--------------------------------------------------------------------------
    #  Bounding box
    #--------------------------------------------------------------------------

    #: Bounding box in screen coordinates
    screen_bbox = Instance(BoundingBox)

    def _screen_bbox_default(self):
        return BoundingBox.from_extents(self.x, self.y, self.x2, self.y2)

    def _size_changed(self):
        if self.container is not None:
            self.container._component_size_changed()
        self._update_bbox()

    def _origin_changed(self):
        if self.container is not None:
            self.container._component_origin_changed()
        self._update_bbox()

    def _update_bbox(self):
        self.screen_bbox.bounds = (self.x, self.y, self.width, self.height)

    #------------------------------------------------------------------------
    # Basic appearance traits
    #------------------------------------------------------------------------

    # The background color of this component.
    bgcolor = ColorTrait('transparent')

    # Is the component visible?
    visible = Bool(True)

    # A read-only property that returns True if this component needs layout.
    layout_needed = Property

    _layout_needed = Bool(True)

    #------------------------------------------------------------------------
    # Abstract methods
    #------------------------------------------------------------------------

    def _do_layout(self):
        """ Called by do_layout() to do an actual layout call; it bypasses some
        additional logic to handle null size and setting **_layout_needed**.
        """
        pass

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def draw(self, gc, view_bounds=None):
        """ Draws the plot component.

        Parameters
        ----------
        gc : Kiva GraphicsContext
            The graphics context to draw the component on
        view_bounds : 4-tuple of integers
            (x, y, width, height) of the area to draw
        """
        if not self.visible:
            return

        if self.layout_needed:
            self.do_layout()

        # XXX: This causes underlays to draw once but overlays twice.
        for layer in self.draw_order:
            self.draw_layer(layer, gc, view_bounds)

    def request_redraw(self):
        """
        Requests that the component redraw itself.  Usually this means asking
        its parent for a repaint.
        """
        if self.container is not None:
            self.container.request_redraw()
        elif self._window:
            self._window.redraw()

    def is_in(self, x, y):
        # A basic implementation of is_in(); subclasses should provide their
        # own if they are more accurate/faster/shinier.
        width, height = self.size
        x_pos, y_pos = self.origin

        return ((x >= x_pos) and (x < (x_pos + width)) and
                (y >= y_pos) and (y < (y_pos + height)))

    def cleanup(self, window):
        """When a window viewing or containing a component is destroyed,
        cleanup is called on the component to give it the opportunity to
        delete any transient state it may have (such as backbuffers)."""
        pass

    #--------------------------------------------------------------------------
    # Serialization interface
    #--------------------------------------------------------------------------

    def serialize(self):
        """Return serialized attributes for this class.
        """
        serialized_children = self._serialize_children()
        serialized_values = self.serialize_shallow()
        values = serialized_values[self.label]

        assert len(set(values).intersection(serialized_children)) == 0
        serialized_values[self.label].update(serialized_children)

        return serialized_values

    def serialize_shallow(self):
        """Return serialized attributes for this class, not including children.
        """
        return {self.label: {}}

    def _iter_children(self):
        """Yield child objects for serialization."""
        return ()

    def _serialize_children(self):
        for child in self._iter_children():
            return {child.label: child.serialize()}
        return {}

    #------------------------------------------------------------------------
    # Layout-related concrete methods
    #------------------------------------------------------------------------

    def do_layout(self, size=None, force=False):
        """ Tells this component to do layout at a given size.

        Always do layout on underlays or overlays, even if `force` is False.

        Parameters
        ----------
        size : (width, height)
            Size at which to lay out the component; either or both values can
            be 0. If it is None, then use `size` for layout
        force : Boolean
            If False, do layout only if `layout_needed` is True.
        """
        if self.layout_needed or force:
            if size is not None:
                self.size = size
            self._do_layout()
            self._layout_needed = False

        for layer in chain(self.underlays, self.overlays):
            if layer.visible:
                layer.do_layout()

    def get_preferred_size(self):
        """ Return the preferred size (width, height) for this component. """
        return [0, 0]

    #------------------------------------------------------------------------
    # Protected methods
    #------------------------------------------------------------------------

    def draw_layer(self, layer, gc, view_bounds):
        """ Renders the named *layer* of this component.

        This method can be used by container classes that group many components
        together and want them to draw cooperatively. The container iterates
        through its components and asks them to draw only certain layers.
        """
        if self.layout_needed:
            self.do_layout()

        handler = getattr(self, "_draw_" + layer, None)
        if handler:
            handler(gc, view_bounds)

    #------------------------------------------------------------------------
    # Protected methods for subclasses to implement
    #------------------------------------------------------------------------

    def _draw_background(self, gc, view_bounds=None):
        """ Draws the background layer of a component.
        """
        if self.bgcolor not in ("clear", "transparent", "none"):
            rect = tuple(self.origin) + (self.width-1, self.height-1)

            with gc:
                gc.set_antialias(False)
                gc.set_fill_color(self.bgcolor_)
                gc.draw_rect(rect, FILL)

    def _draw_overlay(self, gc, view_bounds=None):
        """ Draws the overlay layer of a component.
        """
        for overlay in self.overlays:
            if overlay.visible:
                overlay.draw(self, gc, view_bounds)

    def _draw_underlay(self, gc, view_bounds=None):
        """ Draws the underlay layer of a component.
        """
        for underlay in self.underlays:
            # This method call looks funny but it's correct - underlays are
            # just overlays drawn at a different time in the rendering loop.
            if underlay.visible:
                underlay.draw(self, gc, view_bounds)

    #------------------------------------------------------------------------
    # Tool-related methods and event dispatch
    #------------------------------------------------------------------------

    def dispatch(self, event, suffix):
        """ Dispatches a mouse event based on the current event state.

        If any object in this sequence handles the event, the method returns
        without proceeding any further through the sequence.

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

        inherited = getattr(super(Component, self), 'dispatch', NullDispatch)
        # Dispatch to components in reverse of drawn/added order
        dispatch_chain = (reversed(self.overlays), [inherited],
                          reversed(self.underlays), reversed(self.tools))
        self._dispatch_to_component_chain(dispatch_chain, event, suffix)

    def _dispatch_to_component_chain(self, component_lists, event, suffix):
        for component in chain(*component_lists):
            component.dispatch(event, suffix)
            if event.handled:
                return

    def _get_layout_needed(self):
        return self._layout_needed

    def _tools_items_changed(self):
        self.request_redraw()

    #------------------------------------------------------------------------
    # Traits methods
    #------------------------------------------------------------------------

    def _size_items_changed(self, event):
        if self.container is not None:
            self.container._component_size_changed()

    def _container_changed(self, old, new):
        if new is None:
            self.origin = [0, 0]

    def _origin_items_changed(self, *args):
        if self.container is not None:
            self.container._component_origin_changed()

    def _visible_changed(self, old, new):
        if new:
            self._layout_needed = True

    def _set_window(self, win):
        self._window = win

    def _label_default(self):
        return self.__class__.__name__
