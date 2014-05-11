""" Defines the Plot class.
"""
from traits.api import Dict, Instance, List, Str

from .array_data_source import ArrayDataSource
from .data_canvas import DataCanvas
from .plot_label import PlotLabel
from .utils.data_structures import NoisyDict
from .utils.misc import new_item_name
from .renderer.line_renderer import LineRenderer


class PlotCanvas(DataCanvas):
    """ Represents a correlated set of data, renderers, and axes in a single
    screen region.
    """

    #------------------------------------------------------------------------
    # Data-related traits
    #------------------------------------------------------------------------

    #: The PlotData instance that drives this plot.
    data = Instance(NoisyDict)

    #------------------------------------------------------------------------
    # General plotting traits
    #------------------------------------------------------------------------

    #: Mapping of renderer names to *lists* of plot renderers.
    renderers = Dict(Str, List)

    #------------------------------------------------------------------------
    # Annotations and decorations
    #------------------------------------------------------------------------

    #: The PlotLabel object that contains the title.
    title = Instance(PlotLabel)

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def plot(self, data, **styles):
        """ Adds a new sub-plot using the given data and plot style.

        Returns
        -------
        renderers : list
            Renderers created in response to this call to plot()
        """
        name = new_item_name(self.renderers, name_template='plot_{}')

        x_src = ArrayDataSource(self.data[data[0]])
        self.data_bbox.update_from_x_data(x_src.get_data())

        new_renderers = []
        for y_name in data[1:]:
            y_src = ArrayDataSource(self.data[y_name])
            self.data_bbox.update_from_y_data(y_src.get_data())

            renderer = LineRenderer(x_src=x_src, y_src=y_src,
                                    data_bbox=self.data_bbox, **styles)

            self.add(renderer)
            new_renderers.append(renderer)
        self.renderers[name] = new_renderers

        return self.renderers[name]

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _title_default(self):
        title = PlotLabel(font='modern 16', component=self)
        self.overlays.append(title)
        return title
