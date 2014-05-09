""" Defines the base class for XY plots.
"""
from traits.api import Instance, Property

from ..plot_component import PlotComponent
from ..layout.bounding_box import BoundingBox
from ..layout.bbox_transform import BboxTransform


class BaseRenderer(PlotComponent):
    """ Base class for all renderers.

    Unlike artists, renderers may contain the data that they render. Renderers
    are simply specific types of plots: For example, line-plots, marker-plots,
    and bar-plots, may all be the same data associated with different renderers.
    As a result, renderers may use a few different artists to compose a plot;
    for example, a box-and-whisker plot might have separate artists to draw
    rectangles, error-bars (whiskers), and points (outliers).
    """

    #------------------------------------------------------------------------
    # Data-related traits
    #------------------------------------------------------------------------

    #: Bounding box for data in plot.
    data_bbox = Instance(BoundingBox)

    #: Transform from data space to screen space.
    data_to_screen = Instance(BboxTransform)

    #: Transform from data space to screen space.
    screen_to_data = Property(Instance(BboxTransform),
                              depends_on='data_to_screen')

    def _data_to_screen_default(self):
        return BboxTransform(self.data_bbox, self.screen_bbox)

    def _get_screen_to_data(self):
        return self.data_to_screen.inverted()
