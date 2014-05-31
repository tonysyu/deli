import numpy as np

from traits.api import Callable, Dict, Instance, Property, Str

from .core.container import Container
from .layout.bbox_transform import BboxTransform
from .layout.bounding_box import BoundingBox
from .layout.box_layout import simple_container_do_layout
from .plots.base_plot import BasePlot
from .style import config
from .utils.misc import new_item_name


def replace_in_list(a_list, old, new):
    if old in a_list:
        a_list.remove(old)
    if new is not None:
        a_list.append(new)


class Canvas(Container):
    """ Represents a mapping from 2-D data space into 2-D screen space.

    It can house plots and other plot components, and otherwise behaves
    just like a normal Container.
    """

    bgcolor = config.get('background.canvas.color')

    #: Mapping of plot names to *lists* of plots.
    plots = Dict(Str, Instance(BasePlot))

    # The bounding box containing data added to plot.
    data_bbox = Instance(BoundingBox)

    #: Transform from data space to screen space.
    data_to_screen = Instance(BboxTransform)

    #: Transform from data space to screen space.
    screen_to_data = Property(Instance(BboxTransform),
                              depends_on='data_to_screen')

    #: Layout function which takes the container as the only argument.
    calculate_layout = Callable

    #--------------------------------------------------------------------------
    #  Public interface
    #--------------------------------------------------------------------------

    def add_plot(self, plot, name=None):
        if name is None:
            name = new_item_name(self.plots, name_template='plot_{}')

        self.data_bbox.update_from_extents(*plot.data_extents)
        plot.data_bbox = self.data_bbox
        self.plots[name] = plot
        self.add(plot)

    def replace_underlay(self, old, new):
        replace_in_list(self.underlays, old, new)

    def replace_overlay(self, old, new):
        replace_in_list(self.overlays, old, new)

    #--------------------------------------------------------------------------
    #  Traits properties and defaults
    #--------------------------------------------------------------------------

    def _get_screen_to_data(self):
        return self.data_to_screen.inverted()

    def _data_bbox_default(self):
        return BoundingBox.from_extents(np.inf, np.inf, -np.inf, -np.inf)

    def _data_to_screen_default(self):
        return BboxTransform(self.data_bbox, self.screen_bbox)

    def _calculate_layout_default(self):
        return simple_container_do_layout

    #--------------------------------------------------------------------------
    #  Protected interface
    #--------------------------------------------------------------------------

    def _do_layout(self):
        """ Adjust component layout (called by do_layout()).

        Override Container method to make sure that child components,
        i.e. plots, fill the canvas.
        """
        self.calculate_layout(self)
