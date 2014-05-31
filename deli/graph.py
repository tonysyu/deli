from traits.api import Instance, Int

from .axis import BaseAxis, XAxis, YAxis
from .canvas import Canvas
from .core.container import Container
from .grid import BaseGrid, XGrid, YGrid
from .plot_label import PlotLabel
from .style import config


class Graph(Container):
    """ Represents a correlated set of data, plots, and axes in a single
    screen region.
    """

    # The primary container for plot data.
    canvas = Instance(Canvas)

    margin = Int(config.get('container.graph.margin'))

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

    #: The PlotLabel object that contains the title.
    title = Instance(PlotLabel)

    #--------------------------------------------------------------------------
    # Public interface
    #--------------------------------------------------------------------------

    def __init__(self, **kwtraits):
        super(Graph, self).__init__(**kwtraits)
        self._init_components()
        self.add(self.canvas)

    def add_plot(self, plot, name=None):
        self.canvas.add_plot(plot, name=name)

    #--------------------------------------------------------------------------
    #  Bounding box
    #--------------------------------------------------------------------------

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
        self.canvas.overlays.append(title)
        return title

    def _canvas_default(self):
        return Canvas(screen_bbox=self.screen_bbox)

    #--------------------------------------------------------------------------
    #  Protected interface
    #--------------------------------------------------------------------------

    def _update_bbox(self):
        """ Update bounding box when position or bounds change

        Extend Container method to make sure the canvas is stretched to the
        desired size (based on the graph size and `margin`).
        """
        super(Graph, self)._update_bbox()
        self.canvas.bounds = (w - 2 * self.margin for w in self.bounds)
        self.canvas.position = (self.margin, self.margin)

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _init_components(self):
        if not self.x_grid:
            self.x_grid = XGrid(component=self.canvas)

        if not self.y_grid:
            self.y_grid = YGrid(component=self.canvas)

        if not self.x_axis:
            self.x_axis = XAxis(component=self.canvas)

        if not self.y_axis:
            self.y_axis = YAxis(component=self.canvas)
