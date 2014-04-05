""" Defines the Plot class.
"""
from traits.api import Delegate, Dict, Instance, List, Property, Str

from .abstract_data_source import AbstractDataSource
from .abstract_plot_data import AbstractPlotData
from .array_data_source import ArrayDataSource
from .data_view import DataView
from .lineplot import LinePlot
from .linear_mapper import LinearMapper
from .plot_label import PlotLabel


class Plot(DataView):
    """ Represents a correlated set of data, renderers, and axes in a single
    screen region.
    """

    #------------------------------------------------------------------------
    # Data-related traits
    #------------------------------------------------------------------------

    # The PlotData instance that drives this plot.
    data = Instance(AbstractPlotData)

    # Mapping of data names from self.data to their respective datasources.
    datasources = Dict(Str, Instance(AbstractDataSource))

    #------------------------------------------------------------------------
    # General plotting traits
    #------------------------------------------------------------------------

    # Mapping of plot names to *lists* of plot renderers.
    plots = Dict(Str, List)

    # The default index to use when adding new subplots.
    default_index = Instance(AbstractDataSource)

    #------------------------------------------------------------------------
    # Annotations and decorations
    #------------------------------------------------------------------------

    # The title of the plot.
    title = Property()

    # The font to use for the title.
    title_font = Property()

    # Convenience attribute for title.overlay_position; can be "top",
    # "bottom", "left", or "right".
    title_position = Property()

    # Use delegates to expose the other PlotLabel attributes of the plot title
    title_text = Delegate("_title", prefix="text", modify=True)
    title_color = Delegate("_title", prefix="color", modify=True)
    title_angle = Delegate("_title", prefix="angle", modify=True)

    # The PlotLabel object that contains the title.
    _title = Instance(PlotLabel)

    #------------------------------------------------------------------------
    # Public methods
    #------------------------------------------------------------------------

    def __init__(self, data=None, **kwtraits):
        title = kwtraits.pop("title")
        super(Plot, self).__init__(**kwtraits)
        if data is not None:
            self.data = data

        if not self._title:
            self._title = PlotLabel(font="swiss 16", visible=False,
                                   overlay_position="top", component=self)
        if title is not None:
            self.title = title

        self._plot_ui_info = None

    def plot(self, data, type="line", name=None, index_scale="linear",
             value_scale="linear", origin=None, **styles):
        """ Adds a new sub-plot using the given data and plot style.

        Parameters
        ----------
        data : string, tuple(string), list(string)
            The data to be plotted. The type of plot and the number of
            arguments determines how the arguments are interpreted:

            one item: (line/scatter)
                The data is treated as the value and self.default_index is
                used as the index.  If **default_index** does not exist, one is
                created from arange(len(*data*))
            two or more items: (line/scatter)
                Interpreted as (index, value1, value2, ...).  Each index,value
                pair forms a new plot of the type specified.
            two items: (cmap_scatter)
                Interpreted as (value, color_values).  Uses **default_index**.
            three or more items: (cmap_scatter)
                Interpreted as (index, val1, color_val1, val2, color_val2, ...)

        type : comma-delimited string of "line", "scatter", "cmap_scatter"
            The types of plots to add.
        name : string
            The name of the plot.  If None, then a default one is created
            (usually "plotNNN").
        index_scale : string
            The type of scale to use for the index axis. If not "linear", then
            a log scale is used.
        value_scale : string
            The type of scale to use for the value axis. If not "linear", then
            a log scale is used.
        origin : string
            Which corner the origin of this plot should occupy:
                "bottom left", "top left", "bottom right", "top right"
        styles : series of keyword arguments
            attributes and values that apply to one or more of the
            plot types requested, e.g.,'line_color' or 'line_width'.

        Examples
        --------
        ::

            plot("my_data", type="line", name="myplot", color=lightblue)

            plot(("x-data", "y-data"), type="scatter")

            plot(("x", "y1", "y2", "y3"))

        Returns
        -------
        [renderers] -> list of renderers created in response to this call to plot()
        """
        self.index_scale = index_scale
        self.value_scale = value_scale

        if name is None:
            name = self._make_new_plot_name()
        if origin is None:
            origin = self.default_origin

        # Tie data to the index range
        index = self._get_or_create_datasource(data[0])
        if self.default_index is None:
            self.default_index = index
        self.index_range.add(index)
        data = data[1:]

        # Tie data to the value_range and create the renderer for each data
        new_plots = []
        for value_name in data:
            value = self._get_or_create_datasource(value_name)
            self.value_range.add(value)

            imap = LinearMapper(range=self.index_range,
                        stretch_data=self.index_mapper.stretch_data)
            vmap = LinearMapper(range=self.value_range,
                        stretch_data=self.value_mapper.stretch_data)

            plot = LinePlot(index=index,
                            value=value,
                            index_mapper=imap,
                            value_mapper=vmap,
                            origin = origin,
                            **styles)

            self.add(plot)
            new_plots.append(plot)
        self.plots[name] = new_plots

        return self.plots[name]

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _make_new_plot_name(self):
        """ Returns a string that is not already used as a plot title.
        """
        n = len(self.plots)
        plot_template = "plot%d"
        while True:
            name = plot_template % n
            if name not in self.plots:
                break
            else:
                n += 1
        return name

    def _get_or_create_datasource(self, name):
        """ Returns the data source associated with the given name, or creates
        it if it doesn't exist.
        """
        if name not in self.datasources:
            data = self.data.get_data(name)

            if len(data.shape) == 1:
                ds = ArrayDataSource(data, sort_order="none")
            self.datasources[name] = ds

        return self.datasources[name]

    def __title_changed(self, old, new):
        self._overlay_change_helper(old, new)

    def _set_title(self, text):
        self._title.text = text
        self._title.visible = True
