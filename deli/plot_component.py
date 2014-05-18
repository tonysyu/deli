""" Defines the PlotComponent class.
"""
from traits.api import Instance

from .core.component import Component
from .layout.bounding_box import BoundingBox


DEFAULT_DRAWING_ORDER = ["background", "image", "underlay", "plot",
                         "selection", "border", "annotation", "overlay"]


class PlotComponent(Component):
    """
    PlotComponent is the base class for all plot-related visual components.
    It defines the various methods related to layout and tool handling,
    which virtually every subclass uses or needs to be aware of.

    Several of these top-level layout and draw methods have implementations
    that must not be overridden; instead, subclasses implement various
    protected stub methods.

    The order in which various rendering classes on this component are drawn.
    Note that if this component is placed in a container, in most cases
    the container's draw order is used, since the container calls
    each of its contained components for each rendering pass.
    Typically, the definitions of the layers are:

    1. 'background': Background image, shading
    2. 'image': A special layer for plots that render as images.  This is in
        a separate layer since these plots must all render before non-image
        plots.
    3. 'underlay': Axes and grids
    4. 'plot': The main plot area itself
    5. 'selection': Selected content are rendered above normal plot elements
                    to make them stand out
    6. 'border': Plot borders
    7. 'annotation': Lines and text that are conceptually part of the "plot"
       but need to be rendered on top of everything else in the plot
    8. 'overlay': Legends, selection regions, and other tool-drawn visual
       elements
    """

    draw_order = Instance(list, args=(DEFAULT_DRAWING_ORDER,))

    #--------------------------------------------------------------------------
    #  Bounding box
    #--------------------------------------------------------------------------

    #: Bounding box in screen coordinates
    screen_bbox = Instance(BoundingBox)

    def _screen_bbox_default(self):
        return BoundingBox.from_extents(self.x, self.y, self.x2, self.y2)

    def _bounds_changed(self, old, new):
        super(PlotComponent, self)._bounds_changed(old, new)
        self._update_bbox()

    def _update_bbox(self):
        self.screen_bbox.bounds = (self.x, self.y, self.width, self.height)
