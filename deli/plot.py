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

    # The default x to use when adding new subplots.
    default_x_src = Instance(AbstractDataSource)

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

    def plot(self, data, type="line", **styles):
        """ Adds a new sub-plot using the given data and plot style.

        Returns
        -------
        [renderers] -> list of renderers created in response to this call to plot()
        """
        name = self._make_new_plot_name()

        x_src = self._get_or_create_datasource(data[0])
        if self.default_x_src is None:
            self.default_x_src = x_src
        self.x_range.add(x_src)
        data = data[1:]

        new_plots = []
        for y_name in data:
            y_src = self._get_or_create_datasource(y_name)
            self.y_range.add(y_src)

            imap = LinearMapper(range=self.x_range)
            vmap = LinearMapper(range=self.y_range)

            plot = LinePlot(x_src=x_src,
                            y_src=y_src,
                            x_mapper=imap,
                            y_mapper=vmap,
                            origin = self.origin,
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
