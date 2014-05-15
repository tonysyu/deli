""" Defines the Plot class.
"""
from traits.api import Dict, Instance, List, Str

from .data_canvas import DataCanvas
from .plot_label import PlotLabel
from .style import config
from .utils.misc import new_item_name


class PlotCanvas(DataCanvas):
    """ Represents a correlated set of data, renderers, and axes in a single
    screen region.
    """

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

    def add(self, renderer, name=None):
        if name is None:
            name = new_item_name(self.renderers, name_template='plot_{}')
        super(PlotCanvas, self).add(renderer)
        self.renderers[name] = [renderer]
        self.data_bbox.update_from_extents(*renderer.data_extents)
        renderer.data_bbox = self.data_bbox

    #------------------------------------------------------------------------
    # Private methods
    #------------------------------------------------------------------------

    def _title_default(self):
        title = PlotLabel(font=config.get('title.font'), component=self)
        self.overlays.append(title)
        return title
