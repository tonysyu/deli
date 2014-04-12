""" Defines the base class for XY plots.
"""
from numpy import array, transpose
from matplotlib.transforms import Bbox

from traits.api import Disallow, Instance, Property, Range

from .abstract_mapper import AbstractMapper
from .abstract_plot_renderer import AbstractPlotRenderer
from .abstract_data_source import AbstractDataSource
from .array_data_source import ArrayDataSource


class BaseXYPlot(AbstractPlotRenderer):
    """ Base class for simple X-vs-Y plots that consist of a single x
    data array and a single y data array.

    Subclasses handle the actual rendering, but this base class takes care of
    most of making sure events are wired up between mappers and data or screen
    space changes, etc.
    """

    _ = Disallow

    #------------------------------------------------------------------------
    # Data-related traits
    #------------------------------------------------------------------------

    # The data source to use for the x coordinate.
    x_src = Instance(ArrayDataSource)

    # The data source to use as y points.
    y_src = Instance(AbstractDataSource)

    # Screen mapper for x data.
    x_mapper = Instance(AbstractMapper)

    # Screen mapper for y data
    y_mapper = Instance(AbstractMapper)

    #: Bounding box in screen coordinates.
    screen_bbox = Instance(Bbox)

    #------------------------------------------------------------------------
    # Appearance-related traits
    #------------------------------------------------------------------------

    # Overall alpha value of the image. Ranges from 0.0 for transparent to 1.0
    alpha = Range(0.0, 1.0, 1.0)

    #------------------------------------------------------------------------
    # Convenience readonly properties for common annotations
    #------------------------------------------------------------------------

    # Read-only property for x-axis.
    x_axis = Property
    # Read-only property for y-axis.
    y_axis = Property
    # Read-only property for labels.
    labels = Property

    #------------------------------------------------------------------------
    # Other public traits
    #------------------------------------------------------------------------

    # Overrides the default background color trait in PlotComponent.
    bgcolor = "transparent"

    #------------------------------------------------------------------------
    # Concrete methods below
    #------------------------------------------------------------------------

    def __init__(self, **kwtraits):
        # Handling the setting/initialization of these traits manually because
        # they should be initialized in a certain order.
        priority_traits = {}
        for trait_name in ("x_src", "y_src", "x_mapper", "y_mapper"):
            if trait_name in kwtraits:
                priority_traits[trait_name] = kwtraits.pop(trait_name)
        AbstractPlotRenderer.__init__(self)
        self.set(**priority_traits)
        self.set(**kwtraits)

    #------------------------------------------------------------------------
    # AbstractPlotRenderer interface
    #------------------------------------------------------------------------

    def map_screen(self, data_array):
        """ Maps an array of data points into screen space and returns it as
        an array.

        Implements the AbstractPlotRenderer interface.
        """
        x_ary, y_ary = transpose(data_array)

        sx = self.x_mapper.map_screen(x_ary)
        sy = self.y_mapper.map_screen(y_ary)
        return transpose(array((sx,sy)))

    #------------------------------------------------------------------------
    # PlotComponent interface
    #------------------------------------------------------------------------

    def _draw_plot(self, gc, view_bounds=None, mode="normal"):
        """ Draws the 'plot' layer.
        """
        self._draw_component(gc, view_bounds, mode)

    def _draw_component(self, gc, view_bounds=None, mode="normal"):
        # This method should be folded into self._draw_plot(), but is here for
        # backwards compatibilty with non-draw-order stuff.

        pts = self.get_screen_points()
        self._render(gc, pts)

    #------------------------------------------------------------------------
    # Event handlers
    #------------------------------------------------------------------------

    def _update_mappers(self):
        self.x_mapper.screen_bounds = (self.x, self.x2)
        self.y_mapper.screen_bounds = (self.y, self.y2)

        self.screen_bbox = Bbox.from_extents(self.x, self.y, self.x2, self.y2)

        self.invalidate_draw()

    def _bounds_changed(self, old, new):
        super(BaseXYPlot, self)._bounds_changed(old, new)
        self._update_mappers()
