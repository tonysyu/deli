""" Defines the Plot class.
"""
from traits.api import Bool, Dict, Instance, Str

from .axis import BaseAxis, XAxis, YAxis
from .base_graph import BaseGraph
from .grid import BaseGrid, XGrid, YGrid
from .plot_label import PlotLabel
from .plots.base_plot import BasePlot
from .style import config
from .utils.misc import new_item_name


def replace_in_list(a_list, old, new):
    if old in a_list:
        a_list.remove(old)
    if new is not None:
        a_list.append(new)


class Graph(BaseGraph):
    """ Represents a correlated set of data, plots, and axes in a single
    screen region.
    """

    #------------------------------------------------------------------------
    # Axis and Grids
    #------------------------------------------------------------------------

    # The horizontal axis.
    x_axis = Instance(BaseAxis)

    # The vertical axis.
    y_axis = Instance(BaseAxis)

    # The grid that intersects the x-axis, i.e., a set of vertical lines.
    x_grid = Instance(BaseGrid)

    # The grid that intersects the y-axis, i.e., a set of horizontal lines.
    y_grid = Instance(BaseGrid)

    # Whether to automatically create the x_axis and y_axis if they were not
    # already set by the caller.
    auto_axis = Bool(True)

    # Whether to automatically create the x_grid and y_grid if they were not
    # already set by the caller.
    auto_grid = Bool(True)

    #------------------------------------------------------------------------
    # General plotting traits
    #------------------------------------------------------------------------

    #: Mapping of plot names to *lists* of plots.
    plots = Dict(Str, Instance(BasePlot))

    #------------------------------------------------------------------------
    # Annotations and decorations
    #------------------------------------------------------------------------

    #: The PlotLabel object that contains the title.
    title = Instance(PlotLabel)

    #------------------------------------------------------------------------
    # Appearance
    #------------------------------------------------------------------------

    bgcolor = "white"

    #--------------------------------------------------------------------------
    # Object interface
    #--------------------------------------------------------------------------

    def __init__(self, padding=50, **kwtraits):
        super(BaseGraph, self).__init__(padding=padding, **kwtraits)
        self._init_components()

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def add(self, plot, name=None):
        if name is None:
            name = new_item_name(self.plots, name_template='plot_{}')
        super(Graph, self).add(plot)
        self.plots[name] = plot
        self.data_bbox.update_from_extents(*plot.data_extents)
        plot.data_bbox = self.data_bbox

    #-------------------------------------------------------------------------
    # Event handlers
    #-------------------------------------------------------------------------

    def _x_grid_changed(self, old, new):
        self._replace_underlay(old, new)

    def _y_grid_changed(self, old, new):
        self._replace_underlay(old, new)

    def _x_axis_changed(self, old, new):
        self._replace_underlay(old, new)

    def _y_axis_changed(self, old, new):
        self._replace_underlay(old, new)

    #------------------------------------------------------------------------
    # Traits defaults
    #------------------------------------------------------------------------

    def _title_default(self):
        title = PlotLabel(font=config.get('title.font'), component=self)
        self.overlays.append(title)
        return title

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _init_components(self):
        if not self.x_grid and self.auto_grid:
            self.x_grid = XGrid(component=self)
        if not self.y_grid and self.auto_grid:
            self.y_grid = YGrid(component=self)

        if not self.x_axis and self.auto_axis:
            self.x_axis = XAxis(component=self)

        if not self.y_axis and self.auto_axis:
            self.y_axis = YAxis(component=self)

    def _replace_underlay(self, old, new):
        replace_in_list(self.underlays, old, new)

    def _replace_overlay(self, old, new):
        replace_in_list(self.overlays, old, new)
