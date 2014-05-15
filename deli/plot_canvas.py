""" Defines the Plot class.
"""
from traits.api import Dict, Instance, Str

from .data_canvas import DataCanvas
from .plot_label import PlotLabel
from .plots.base_plot import BasePlot
from .style import config
from .utils.misc import new_item_name


class PlotCanvas(DataCanvas):
    """ Represents a correlated set of data, plots, and axes in a single
    screen region.
    """

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
    # Public methods
    #------------------------------------------------------------------------

    def add(self, plot, name=None):
        if name is None:
            name = new_item_name(self.plots, name_template='plot_{}')
        super(PlotCanvas, self).add(plot)
        self.plots[name] = plot
        self.data_bbox.update_from_extents(*plot.data_extents)
        plot.data_bbox = self.data_bbox

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _title_default(self):
        title = PlotLabel(font=config.get('title.font'), component=self)
        self.overlays.append(title)
        return title
