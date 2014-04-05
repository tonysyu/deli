""" Defines the base class for XY plots.
"""
from numpy import array, transpose

from traits.api import Array, Bool, Enum, Instance, Property, Range

from .abstract_mapper import AbstractMapper
from .abstract_plot_renderer import AbstractPlotRenderer
from .abstract_data_source import AbstractDataSource
from .array_data_source import ArrayDataSource


class BaseXYPlot(AbstractPlotRenderer):
    """ Base class for simple X-vs-Y plots that consist of a single index
    data array and a single value data array.

    Subclasses handle the actual rendering, but this base class takes care of
    most of making sure events are wired up between mappers and data or screen
    space changes, etc.
    """

    #------------------------------------------------------------------------
    # Data-related traits
    #------------------------------------------------------------------------

    # The data source to use for the index coordinate.
    index = Instance(ArrayDataSource)

    # The data source to use as value points.
    value = Instance(AbstractDataSource)

    # Screen mapper for index data.
    index_mapper = Instance(AbstractMapper)
    # Screen mapper for value data
    value_mapper = Instance(AbstractMapper)

    # Corresponds to **index_mapper**
    x_mapper = Property
    # Corresponds to **value_mapper**
    y_mapper = Property

    # Convenience property for accessing the index data range.
    index_range = Property
    # Convenience property for accessing the value data range.
    value_range = Property

    #------------------------------------------------------------------------
    # Appearance-related traits
    #------------------------------------------------------------------------

    # The orientation of the index axis.
    orientation = Enum("h", "v")

    # Overall alpha value of the image. Ranges from 0.0 for transparent to 1.0
    alpha = Range(0.0, 1.0, 1.0)

    #------------------------------------------------------------------------
    # Convenience readonly properties for common annotations
    #------------------------------------------------------------------------

    # Read-only property for horizontal grid.
    hgrid = Property
    # Read-only property for vertical grid.
    vgrid = Property
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
    # Private traits
    #------------------------------------------------------------------------

    # Are the cache traits valid? If False, new ones need to be compute.
    _cache_valid = Bool(False)

    # Cached array of (x,y) data-space points; regardless of self.orientation,
    # these points are always stored as (index_pt, value_pt).
    _cached_data_pts = Array

    # Cached array of (x,y) screen-space points.
    _cached_screen_pts = Array

    # Does **_cached_screen_pts** contain the screen-space coordinates
    # of the points currently in **_cached_data_pts**?
    _screen_cache_valid = Bool(False)

    #------------------------------------------------------------------------
    # Concrete methods below
    #------------------------------------------------------------------------

    def __init__(self, **kwtraits):
        # Handling the setting/initialization of these traits manually because
        # they should be initialized in a certain order.
        priority_traits = {"trait_change_notify": False}
        for trait_name in ("index", "value", "index_mapper", "value_mapper"):
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

        sx = self.index_mapper.map_screen(x_ary)
        sy = self.value_mapper.map_screen(y_ary)
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
    # Properties
    #------------------------------------------------------------------------

    def _get_index_range(self):
        return self.index_mapper.range

    def _get_value_range(self):
        return self.value_mapper.range

    #------------------------------------------------------------------------
    # Event handlers
    #------------------------------------------------------------------------

    def _update_mappers(self):
        x_mapper = self.index_mapper
        y_mapper = self.value_mapper

        x = self.x
        x2 = self.x2
        y = self.y
        y2 = self.y2

        x_mapper.screen_bounds = (x, x2)
        y_mapper.screen_bounds = (y, y2)

        self.invalidate_draw()
        self._cache_valid = False
        self._screen_cache_valid = False

    def _bounds_changed(self, old, new):
        super(BaseXYPlot, self)._bounds_changed(old, new)
        self._update_mappers()
