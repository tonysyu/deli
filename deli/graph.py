""" Defines the Plot class.
"""
from traits.api import Bool, Dict, Instance, Int, Str

from .axis import BaseAxis, XAxis, YAxis
from .canvas import Canvas
from .core.container import Container
from .grid import BaseGrid, XGrid, YGrid
from .plot_label import PlotLabel
from .plots.base_plot import BasePlot
from .style import config
from .utils.misc import new_item_name


class Graph(Container):
    """ Represents a correlated set of data, plots, and axes in a single
    screen region.
    """

    # The primary container for plot data.
    canvas = Instance(Canvas)

    margin = Int(config.get('container.graph.margin'))

    #--------------------------------------------------------------------------
    #  Bounding box
    #--------------------------------------------------------------------------

    def _update_bbox(self):
        self.screen_bbox.bounds = (self.x, self.y, self.width, self.height)
        self.canvas.bounds = (w - 2 * self.margin for w in self.bounds)
        self.canvas.position = (self.margin, self.margin)

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

    #--------------------------------------------------------------------------
    # Object interface
    #--------------------------------------------------------------------------

    def __init__(self, **kwtraits):
        super(Graph, self).__init__(**kwtraits)
        self._init_components()
        self.add(self.canvas)

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def add_plot(self, plot, name=None):
        if name is None:
            name = new_item_name(self.plots, name_template='plot_{}')
        self.canvas.add_plot(plot)
        self.plots[name] = plot

    #-------------------------------------------------------------------------
    # Event handlers
    #-------------------------------------------------------------------------

    def _x_grid_changed(self, old, new):
        self.canvas.replace_underlay(old, new)

    def _y_grid_changed(self, old, new):
        self.canvas.replace_underlay(old, new)

    def _x_axis_changed(self, old, new):
        self.canvas.replace_underlay(old, new)

    def _y_axis_changed(self, old, new):
        self.canvas.replace_underlay(old, new)

    #------------------------------------------------------------------------
    # Traits defaults
    #------------------------------------------------------------------------

    def _title_default(self):
        title = PlotLabel(font=config.get('title.font'), component=self.canvas)
        self.overlays.append(title)
        return title

    def _canvas_default(self):
        return Canvas(screen_bbox=self.screen_bbox)

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _init_components(self):
        if not self.x_grid and self.auto_grid:
            self.x_grid = XGrid(component=self.canvas)
        if not self.y_grid and self.auto_grid:
            self.y_grid = YGrid(component=self.canvas)

        if not self.x_axis and self.auto_axis:
            self.x_axis = XAxis(component=self.canvas)

        if not self.y_axis and self.auto_axis:
            self.y_axis = YAxis(component=self.canvas)
