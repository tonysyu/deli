from traits.api import Instance, Int

from .axis import BaseAxis, XAxis, YAxis
from .canvas import Canvas
from .core.container import Container
from .grid import BaseGrid, XGrid, YGrid
from .plot_label import PlotLabel
from .style import config


class Graph(Container):
    """ Container a plot canvas and surrounding decorations. """

    # The primary container for plot data.
    canvas = Instance(Canvas)

    margin = Int(config.get('container.graph.margin'))

    # -----------------------------------------------------------------------
    # Axis and Grids
    # -----------------------------------------------------------------------

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

    # -------------------------------------------------------------------------
    # Public interface
    # -------------------------------------------------------------------------

    def __init__(self, **kwtraits):
        super(Graph, self).__init__(**kwtraits)
        self._init_components()
        self.add(self.canvas)

    def add_artist(self, artist, name=None):
        self.canvas.add_artist(artist, name=name)

    # ------------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------------

    def _x_grid_changed(self, old, new):
        self.canvas.replace_underlay(old, new)

    def _y_grid_changed(self, old, new):
        self.canvas.replace_underlay(old, new)

    def _x_axis_changed(self, old, new):
        self.canvas.replace_underlay(old, new)

    def _y_axis_changed(self, old, new):
        self.canvas.replace_underlay(old, new)

    # -----------------------------------------------------------------------
    # Traits defaults
    # -----------------------------------------------------------------------

    def _title_default(self):
        title = PlotLabel(font=config.get('title.font'), component=self.canvas)
        self.canvas.overlays.append(title)
        return title

    def _canvas_default(self):
        return Canvas()

    # -------------------------------------------------------------------------
    #  Protected interface
    # -------------------------------------------------------------------------

    def _update_bbox(self):
        """ Update bounding box when origin or size changes.

        Extend Container method to make sure the canvas is stretched to the
        desired size (based on the graph size and `margin`).
        """
        super(Graph, self)._update_bbox()
        self.canvas.size = (w - 2 * self.margin for w in self.size)
        self.canvas.origin = (self.margin, self.margin)

    # -----------------------------------------------------------------------
    # Private methods
    # -----------------------------------------------------------------------

    def _init_components(self):
        artist_kwargs = {'parent': self.canvas,
                         'data_bbox': self.canvas.data_bbox,
                         'screen_bbox': self.canvas.local_bbox}

        if not self.x_grid:
            self.x_grid = XGrid(**artist_kwargs)
        if not self.y_grid:
            self.y_grid = YGrid(**artist_kwargs)
        if not self.x_axis:
            self.x_axis = XAxis(**artist_kwargs)
        if not self.y_axis:
            self.y_axis = YAxis(**artist_kwargs)
