""" Defines the base class for artists.
"""
from contextlib import contextmanager

from traits.api import Instance, Property, Tuple

from ..core.component import Component
from ..layout.bounding_box import BoundingBox
from ..layout.bbox_transform import BboxTransform


class BaseArtist(Component):
    """ Base class for all artists.

    Unlike styluses, artists contain the data that they render. Artists are
    simply specific types of plots: For example, line artists, marker artists,
    and bar artists, all operate on the same type of data, but those artist
    will render the data differently.

    Artists may use a few different styluses to compose a plot; for example,
    a box-and-whisker artist might have separate styluses to draw rectangles,
    error-bars (whiskers), and points (outliers).
    """

    # -----------------------------------------------------------------------
    # Data-related traits
    # -----------------------------------------------------------------------

    #: The extents of the data (x_min, y_min, x_max, y_max)
    data_extents = Property(Tuple)

    #: Styluses associated with this artist.
    styluses = Property(Tuple)

    #: Bounding box for data in the graph. Note that this bounding box
    #: does not just describe the data in this artist; it's the currently
    #: displayed limits of the plot in data space.
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

    # -------------------------------------------------------------------------
    #  BaseArtist interface
    # -------------------------------------------------------------------------

    def _get_data_extents(self):
        msg = "`BaseArtist` subclasses must implement `_get_data_extents`"
        raise NotImplementedError(msg)

    def _container_changed(self):
        if self.container is not None:
            self.data_bbox = self.container.data_bbox
            self.screen_bbox = self.container.local_bbox

    @contextmanager
    def _clipped_context(self, gc):
        with gc:
            gc.clip_to_rect(*self.screen_bbox.rect)
            yield
