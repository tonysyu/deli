""" Defines the Component class """
from itertools import chain

import numpy as np

from enable.colors import white_color_trait
from kiva.constants import FILL
from traits.api import Any, Bool, Float, Instance, Int, List, Property, Trait

from .coordinate_box import CoordinateBox


DRAWING_ORDER = ['background', 'underlay', 'border', 'overlay']


class NullDispatch(object):

    @staticmethod
    def dispatch(event, suffix):
        pass


class Component(CoordinateBox):
    """ Component is the base class for most objects.

    Since Components can have a border and padding, there is an additional set
    of bounds and position attributes to define the "outer box" of components.
    """

    #------------------------------------------------------------------------
    # Components and containers
    #------------------------------------------------------------------------

    # The parent container for this component.
    container = Any    # Instance("Container")

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

    #------------------------------------------------------------------------
    # Basic appearance traits
    #------------------------------------------------------------------------

    # The background color of this component.
    bgcolor = white_color_trait

    # Is the component visible?
    visible = Bool(True)

    # Does the component use space in the layout even if it is not visible?
    invisible_layout = Bool(False)

    # The width of the border around this component.
    border_width = Int(1)

    # Visibility of border.
    border_visible = Bool(False)

    #------------------------------------------------------------------------
    # Layout traits
    #------------------------------------------------------------------------

    # The ratio of the component's width to its height.
    aspect_ratio = Trait(None, None, Float)

    # A read-only property that returns True if this component needs layout.
    layout_needed = Property

    _layout_needed = Bool(True)

    # The amount of space to put on the left side of the component
    padding_left = Int(0)

    # The amount of space to put on the right side of the component
    padding_right = Int(0)

    # The amount of space to put on top of the component
    padding_top = Int(0)

    # The amount of space to put below the component
    padding_bottom = Int(0)

    # This property allows a way to set the padding in bulk. It can either be
    # set to a single Int (which sets padding on all sides) or a tuple/list of
    # 4 Ints representing the (left, right, top, bottom) padding amounts.
    padding = Property

    # Readonly property expressing the total amount of horizontal padding
    hpadding = Property

    # Readonly property expressing the total amount of vertical padding
    vpadding = Property

    # The lower left corner of the padding outer box around the component.
    outer_position = Property

    # The number of horizontal and vertical pixels in the padding outer box.
    outer_bounds = Property

    #------------------------------------------------------------------------
    # Abstract methods
    #------------------------------------------------------------------------

    def _do_layout(self):
        """ Called by do_layout() to do an actual layout call; it bypasses some
        additional logic to handle null bounds and setting **_layout_needed**.
        """
        pass

    def _draw_component(self, gc, view_bounds=None):
        """ Renders the component.

        Subclasses must implement this method to actually render themselves.
        Note: This method is used only by the "old" drawing calls.
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

    def is_in(self, x, y, include_padding=True):
        # A basic implementation of is_in(); subclasses should provide their
        # own if they are more accurate/faster/shinier.
        if include_padding:
            width, height = self.outer_bounds
            x_pos, y_pos = self.outer_position
        else:
            width, height = self.bounds
            x_pos, y_pos = self.position

        return ((x >= x_pos) and (x < (x_pos + width)) and
                (y >= y_pos) and (y < (y_pos + height)))

    def cleanup(self, window):
        """When a window viewing or containing a component is destroyed,
        cleanup is called on the component to give it the opportunity to
        delete any transient state it may have (such as backbuffers)."""
        pass

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
            be 0. If it is None, then use `bounds` for layout
        force : Boolean
            If False, do layout only if `layout_needed` is True.
        """
        if self.layout_needed or force:
            if size is not None:
                self.bounds = size
            self._do_layout()
            self._layout_needed = False

        for layer in chain(self.underlays, self.overlays):
            if layer.visible or layer.invisible_layout:
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
        # Don't render the selection layer if use_selection is false.  This
        # is mostly for backwards compatibility.
        if self.layout_needed:
            self.do_layout()

        handler = getattr(self, "_draw_" + layer, None)
        if handler:
            handler(gc, view_bounds)

    def _draw_border(self, gc, view_bounds=None):
        """ Utility method to draw the borders around this component. """
        pass

    #------------------------------------------------------------------------
    # Protected methods for subclasses to implement
    #------------------------------------------------------------------------

    def _draw_background(self, gc, view_bounds=None):
        """ Draws the background layer of a component.
        """
        if self.bgcolor not in ("clear", "transparent", "none"):
            rect = tuple(self.position) + (self.width-1, self.height-1)

            with gc:
                gc.set_antialias(False)
                gc.set_fill_color(self.bgcolor_)
                gc.draw_rect(rect, FILL)

    def _draw_overlay(self, gc, view_bounds=None):
        """ Draws the overlay layer of a component.
        """
        for overlay in self.overlays:
            if overlay.visible:
                overlay.overlay(self, gc, view_bounds)

    def _draw_underlay(self, gc, view_bounds=None):
        """ Draws the underlay layer of a component.
        """
        for underlay in self.underlays:
            # This method call looks funny but it's correct - underlays are
            # just overlays drawn at a different time in the rendering loop.
            if underlay.visible:
                underlay.overlay(self, gc, view_bounds)

    def _get_visible_border(self):
        """ Helper function to return the amount of border, if visible """
        return self.border_width if self.border_visible else 0

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
    # Event handlers
    #------------------------------------------------------------------------

    def _bounds_changed(self, old, new):
        if self.container is not None:
            self.container._component_bounds_changed(self)

    def _bounds_items_changed(self, event):
        if self.container is not None:
            self.container._component_bounds_changed(self)

    def _container_changed(self, old, new):
        if new is None:
            self.position = [0,0]

    def _position_changed(self, *args):
        if self.container is not None:
            self.container._component_position_changed(self)

    def _position_items_changed(self, *args):
        if self.container is not None:
            self.container._component_position_changed(self)

    def _visible_changed(self, old, new):
        if new:
            self._layout_needed = True

    def _set_window(self, win):
        self._window = win

    #------------------------------------------------------------------------
    # Position and padding setters and getters
    #------------------------------------------------------------------------

    def _get_x(self):
        return self.position[0]

    def _set_x(self, val):
        self.position[0] = val

    def _get_y(self):
        return self.position[1]

    def _set_y(self, val):
        self.position[1] = val

    def _get_hpadding(self):
        border_size = 2 * self._get_visible_border()
        return border_size + self.padding_right + self.padding_left

    def _get_vpadding(self):
        border_size = 2 * self._get_visible_border()
        return border_size + self.padding_bottom + self.padding_top

    def _set_padding(self, value):
        if np.isscalar(value):
            value = [value] * 4
        self.padding_left, self.padding_right = value[:2]
        self.padding_top, self.padding_bottom = value[2:]

    #------------------------------------------------------------------------
    # Outer position setters and getters
    #------------------------------------------------------------------------

    def _get_outer_position(self):
        border = self._get_visible_border()
        pos = self.position
        return (pos[0] - self.padding_left - border,
                pos[1] - self.padding_bottom - border)

    def _set_outer_position(self, new_pos):
        border = self._get_visible_border()
        self.position = [new_pos[0] + self.padding_left + border,
                         new_pos[1] + self.padding_bottom + border]

    #------------------------------------------------------------------------
    # Outer bounds setters and getters
    #------------------------------------------------------------------------

    def _get_outer_bounds(self):
        bounds = self.bounds
        return (bounds[0] + self.hpadding, bounds[1] + self.vpadding)

    def _set_outer_bounds(self, bounds):
        self.bounds = [bounds[0] - self.hpadding, bounds[1] - self.vpadding]
