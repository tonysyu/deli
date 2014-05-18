""" Defines the Component class """
import numpy as np

from enable.colors import black_color_trait, white_color_trait
from enable.enable_traits import LineStyle
from kiva.constants import FILL
from traits.api import (Any, Bool, Float, Instance, Int, List,
                        Property, Str, Trait)

from .coordinate_box import CoordinateBox
from .interactor import Interactor


DRAWING_ORDER = ['background', 'underlay', 'border', 'overlay']


class Component(CoordinateBox, Interactor):
    """
    Component is the base class for most Enable objects.  In addition to the
    basic position and container features of Component, it also supports
    Viewports and has finite bounds.

    Since Components can have a border and padding, there is an additional set
    of bounds and position attributes that define the "outer box" of the
    components. These cannot be set, since they are secondary attributes
    (computed from the component's "inner" size and margin-area attributes).
    """

    #------------------------------------------------------------------------
    # Basic appearance traits
    #------------------------------------------------------------------------

    # Is the component visible?
    visible = Bool(True)

    # Does the component use space in the layout even if it is not visible?
    invisible_layout = Bool(False)

    # Fill the padding area with the background color?
    fill_padding = Bool(False)

    #------------------------------------------------------------------------
    # Object/containment hierarchy traits
    #------------------------------------------------------------------------

    # Our container object
    container = Any    # Instance("Container")

    # A reference to our top-level Enable Window.  This is stored as a shadow
    # attribute if this component is the direct child of the Window; otherwise,
    # the getter function recurses up the containment hierarchy.
    window = Property   # Instance("Window")

    #------------------------------------------------------------------------
    # Layout traits
    #------------------------------------------------------------------------

    # The ratio of the component's width to its height.  This is used by
    # the component itself to maintain bounds when the bounds are changed
    # independently, and is also used by the layout system.
    aspect_ratio = Trait(None, None, Float)

    # When the component's bounds are set to a (width,height) tuple that does
    # not conform to the set aspect ratio, does the component center itself
    # in the free space?
    auto_center = Bool(True)

    # A read-only property that returns True if this component needs layout.
    # It is a reflection of both the value of the component's private
    # _layout_needed attribute as well as any logical layout dependencies with
    # other components.
    layout_needed = Property

    #------------------------------------------------------------------------
    # Overlays and underlays
    #------------------------------------------------------------------------

    # A list of underlays for this plot.  By default, underlays get a chance to
    # draw onto the plot area underneath plot itself but above any images and
    # backgrounds of the plot.
    underlays = List  #[AbstractOverlay]

    # A list of overlays for the plot.  By default, overlays are drawn above the
    # plot and its annotations.
    overlays = List   #[AbstractOverlay]

    #------------------------------------------------------------------------
    # Padding-related traits
    # Padding in each dimension is defined as the number of pixels that are
    # part of the component but outside of its position and bounds.  Containers
    # need to be aware of padding when doing layout, object collision/overlay
    # calculations, etc.
    #------------------------------------------------------------------------

    # The amount of space to put on the left side of the component
    padding_left = Int(0)

    # The amount of space to put on the right side of the component
    padding_right = Int(0)

    # The amount of space to put on top of the component
    padding_top = Int(0)

    # The amount of space to put below the component
    padding_bottom = Int(0)

    # This property allows a way to set the padding in bulk.  It can either be
    # set to a single Int (which sets padding on all sides) or a tuple/list of
    # 4 Ints representing the left, right, top, bottom padding amounts.  When
    # it is read, this property always returns the padding as a list of four
    # elements even if they are all the same.
    padding = Property

    # Readonly property expressing the total amount of horizontal padding
    hpadding = Property

    # Readonly property expressing the total amount of vertical padding
    vpadding = Property

    # Does the component respond to mouse events over the padding area?
    padding_accepts_focus = Bool(True)

    #------------------------------------------------------------------------
    # Position and bounds of outer box (encloses the padding and border area)
    #------------------------------------------------------------------------

    # The x,y point of the lower left corner of the padding outer box around
    # the component.  Setting this position will move the component, but
    # will not change the padding or bounds.
    outer_position = Property

    # The number of horizontal and vertical pixels in the padding outer box.
    # Setting these bounds will modify the bounds of the component, but
    # will not change the lower-left position (self.outer_position) or
    # the padding.
    outer_bounds = Property

    #------------------------------------------------------------------------
    # Rendering control traits
    #------------------------------------------------------------------------

    # The order in which various rendering classes on this component are drawn.
    # Note that if this component is placed in a container, in most cases
    # the container's draw order is used, since the container calls
    # each of its contained components for each rendering pass.
    # Typically, the definitions of the layers are:
    #
    # #. 'background': Background image, shading, and (possibly) borders
    # #. 'border': A special layer for rendering the border on top of the
    #     component instead of under its main layer (see **overlay_border**)
    # #. 'overlay': Legends, selection regions, and other tool-drawn visual
    #     elements
    draw_order = Instance(list, args=(DRAWING_ORDER,))

    # Draw the border as part of the overlay layer? If False, draw the
    # border as part of the background layer.
    overlay_border = Bool(True)

    #------------------------------------------------------------------------
    # Border and background traits
    #------------------------------------------------------------------------

    # The width of the border around this component.  This is taken into account
    # during layout, but only if the border is visible.
    border_width = Int(1)

    # Is the border visible?  If this is false, then all the other border
    # properties are not used.
    border_visible = Bool(False)

    # The line style (i.e. dash pattern) of the border.
    border_dash = LineStyle

    # The color of the border.  Only used if border_visible is True.
    border_color = black_color_trait

    # The background color of this component.  By default all components have
    # a white background.  This can be set to "transparent" or "none" if the
    # component should be see-through.
    bgcolor = white_color_trait

    #------------------------------------------------------------------------
    # New layout/object containment hierarchy traits
    # These are not used yet.
    #------------------------------------------------------------------------

    # The optional element ID of this component.
    id = Str("")

    #------------------------------------------------------------------------
    # Private traits
    #------------------------------------------------------------------------

    # Shadow trait for self.window.  Only gets set if this is the top-level
    # enable component in a Window.
    _window = Any    # Instance("Window")

    # Whether or not component itself needs to be laid out.  Some times
    # components are composites of others, in which case the layout
    # invalidation relationships should be implemented in layout_needed.
    _layout_needed = Bool(True)

    #------------------------------------------------------------------------
    # Abstract methods
    #------------------------------------------------------------------------

    def _do_layout(self):
        """ Called by do_layout() to do an actual layout call; it bypasses some
        additional logic to handle null bounds and setting **_layout_needed**.
        """
        pass

    def _draw_component(self, gc, view_bounds=None, mode="normal"):
        """ Renders the component.

        Subclasses must implement this method to actually render themselves.
        Note: This method is used only by the "old" drawing calls.
        """
        pass

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def draw(self, gc, view_bounds=None, mode="default"):
        """ Draws the plot component.

        Parameters
        ----------
        gc : Kiva GraphicsContext
            The graphics context to draw the component on
        view_bounds : 4-tuple of integers
            (x, y, width, height) of the area to draw
        mode : string
            The drawing mode to use; can be one of:

            'normal'
                Normal, antialiased, high-quality rendering
            'overlay'
                The plot component is being rendered over something else,
                so it renders more quickly, and possibly omits rendering
                its background and certain tools
            'interactive'
                The plot component is being asked to render in
                direct response to realtime user interaction, and needs to make
                its best effort to render as fast as possible, even if there is
                an aesthetic cost.
        """
        if self.layout_needed:
            self.do_layout()

        self._draw(gc, view_bounds, mode)

    def request_redraw(self):
        """
        Requests that the component redraw itself.  Usually this means asking
        its parent for a repaint.
        """
        self._request_redraw()

    def invalidate_draw(self, self_relative=False):
        """ Invalidates any backbuffer that may exist, and notifies our parents
        of any damaged regions.

        Call this method whenever a component's internal state
        changes such that it must be redrawn on the next draw() call.
        """
        if self.container is not None:
            self.container.invalidate_draw(self_relative=True)

        if self._window is not None:
            self._window.invalidate_draw(self_relative=True)

    def invalidate_and_redraw(self):
        """Convenience method to invalidate our contents and request redraw"""
        self.invalidate_draw()
        self.request_redraw()

    def is_in(self, x, y):
        # A basic implementation of is_in(); subclasses should provide their
        # own if they are more accurate/faster/shinier.
        if self.padding_accepts_focus:
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

        Parameters
        ----------
        size : (width, height)
            Size at which to lay out the component; either or both values can
            be 0. If it is None, then the component lays itself out using
            **bounds**.
        force : Boolean
            Whether to force a layout operation. If False, the component does
            a layout on itself only if **_layout_needed** is True.
            The method always does layout on any underlays or overlays it has,
            even if *force* is False.

        """
        if self.layout_needed or force:
            if size is not None:
                self.bounds = size
            self._do_layout()
            self._layout_needed = False
        for underlay in self.underlays:
            if underlay.visible or underlay.invisible_layout:
                underlay.do_layout()
        for overlay in self.overlays:
            if overlay.visible or overlay.invisible_layout:
                overlay.do_layout()

    def get_preferred_size(self):
        """ Returns the size (width,height) that is preferred for this component
        """
        size = [0, 0]
        return size

    #------------------------------------------------------------------------
    # Protected methods
    #------------------------------------------------------------------------

    def _request_redraw(self):
        if self.container is not None:
            self.container.request_redraw()
        elif self._window:
            self._window.redraw()

    def _draw(self, gc, view_bounds=None, mode="default"):
        """ Draws the component, paying attention to **draw_order**, including
        overlays, underlays, and the like.

        This method is the main draw handling logic in plot components.
        The reason for implementing _draw() instead of overriding the top-level
        draw() method is that the Enable base classes may do things in draw()
        that mustn't be interfered with (e.g., the Viewable mix-in).

        """
        if not self.visible:
            return

        if self.layout_needed:
            self.do_layout()

        for layer in self.draw_order:
            self._dispatch_draw(layer, gc, view_bounds, mode)

    def _dispatch_draw(self, layer, gc, view_bounds, mode):
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
            handler(gc, view_bounds, mode)

    def _draw_border(self, gc, view_bounds=None, mode="default"):
        """ Utility method to draw the borders around this component. """
        pass

    #------------------------------------------------------------------------
    # Protected methods for subclasses to implement
    #------------------------------------------------------------------------

    def _draw_background(self, gc, view_bounds=None, mode="default"):
        """ Draws the background layer of a component.
        """
        if self.bgcolor not in ("clear", "transparent", "none"):
            if self.fill_padding:
                size = (self.outer_width-1, self.outer_height-1)
                rect = tuple(self.outer_position) + size
            else:
                rect = tuple(self.position) + (self.width-1, self.height-1)

            with gc:
                gc.set_antialias(False)
                gc.set_fill_color(self.bgcolor_)
                gc.draw_rect(rect, FILL)

    def _draw_overlay(self, gc, view_bounds=None, mode="normal"):
        """ Draws the overlay layer of a component.
        """
        for overlay in self.overlays:
            if overlay.visible:
                overlay.overlay(self, gc, view_bounds, mode)

    def _draw_underlay(self, gc, view_bounds=None, mode="normal"):
        """ Draws the underlay layer of a component.
        """
        for underlay in self.underlays:
            # This method call looks funny but it's correct - underlays are
            # just overlays drawn at a different time in the rendering loop.
            if underlay.visible:
                underlay.overlay(self, gc, view_bounds, mode)

    def _get_visible_border(self):
        """ Helper function to return the amount of border, if visible """
        return self.border_width if self.border_visible else 0

    #------------------------------------------------------------------------
    # Tool-related methods and event dispatch
    #------------------------------------------------------------------------

    def dispatch(self, event, suffix):
        """ Dispatches a mouse event based on the current event state.

        If the component has a **controller**, the method dispatches the event
        to it, and returns. Otherwise, the following objects get a chance to
        handle the event:

        1. The component's active tool, if any.
        2. Any overlays, in reverse order that they were added and are drawn.
        3. The component itself.
        4. Any underlays, in reverse order that they were added and are drawn.
        5. Any listener tools.

        If any object in this sequence handles the event, the method returns
        without proceeding any further through the sequence. If nothing
        handles the event, the method simply returns.

        Parameters
        ----------
        event : an Enable MouseEvent
            A mouse event.
        suffix : string
            The name of the mouse event as a suffix to the event state name,
            e.g. "_left_down" or "_window_enter".

        """
        if event.handled:
            return

        # Dispatch to overlays in reverse of draw/added order
        for overlay in self.overlays[::-1]:
            overlay.dispatch(event, suffix)
            if event.handled:
                break

        if not event.handled:
            self._dispatch_stateful_event(event, suffix)

        if not event.handled:
            # Dispatch to underlays in reverse of draw/added order
            for underlay in self.underlays[::-1]:
                underlay.dispatch(event, suffix)
                if event.handled:
                    break

        # Now that everyone who might veto/handle the event has had a chance
        # to receive it, dispatch it to our list of listener tools.
        if not event.handled:
            for tool in self.tools:
                tool.dispatch(event, suffix)

    def _get_layout_needed(self):
        return self._layout_needed

    def _tools_items_changed(self):
        self.invalidate_and_redraw()

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
