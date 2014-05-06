""" Defines the Plot class.
"""
from traits.api import Dict, Instance, List, Property, Str

from .abstract_data_source import AbstractDataSource
from .array_data_source import ArrayDataSource
from .data_view import DataView
from .plot_label import PlotLabel
from .utils.data_structures import NoisyDict
from .utils.misc import new_item_name
from .renderer.line_renderer import LineRenderer


class Plot(DataView):
    """ Represents a correlated set of data, renderers, and axes in a single
    screen region.
    """

    #------------------------------------------------------------------------
    # Data-related traits
    #------------------------------------------------------------------------

    # The PlotData instance that drives this plot.
    data = Instance(NoisyDict)

    # Mapping of data names from self.data to their respective datasources.
    datasources = Dict(Str, Instance(AbstractDataSource))

    #------------------------------------------------------------------------
    # General plotting traits
    #------------------------------------------------------------------------

    # Mapping of renderer names to *lists* of plot renderers.
    renderers = Dict(Str, List)

    #------------------------------------------------------------------------
    # Annotations and decorations
    #------------------------------------------------------------------------

    # The title of the plot.
    title = Property()

    # The PlotLabel object that contains the title.
    _title = Instance(PlotLabel)

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def __init__(self, data=None, **kwtraits):
        title = kwtraits.pop('title')
        super(Plot, self).__init__(**kwtraits)
        if data is not None:
            self.data = data

        # This doesn't work when moved to a trait-default definition (Why?)
        self._title= PlotLabel(font="swiss 16", visible=False, component=self)
        if title is not None:
            self.title = title

    def plot(self, data, **styles):
        """ Adds a new sub-plot using the given data and plot style.

        Returns
        -------
        renderers : list
            Renderers created in response to this call to plot()
        """
        name = new_item_name(self.renderers, name_template='plot_{}')

        x_src = self._get_or_create_datasource(data[0])
        self.data_bbox.update_from_x_data(x_src.get_data())
        data = data[1:]

        new_renderers = []
        for y_name in data:
            y_src = self._get_or_create_datasource(y_name)
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

    def _get_or_create_datasource(self, name):
        """ Returns the data source associated with the given name, or creates
        it if it doesn't exist.
        """
        if name not in self.datasources:
            data = self.data[name]

            if len(data.shape) == 1:
                ds = ArrayDataSource(data)
            self.datasources[name] = ds

        return self.datasources[name]

    def __title_changed(self, old, new):
        self._overlay_change_helper(old, new)

    def _set_title(self, text):
        self._title.text = text
        self._title.visible = True
