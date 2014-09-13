import numpy as np

from traits.api import Callable, Dict, Instance, Property, Str

from .artist.base_artist import BaseArtist
from .core.container import Container
from .layout.bbox_transform import BboxTransform
from .layout.bounding_box import BoundingBox
from .layout.box_layout import simple_container_do_layout
from .style import config
from .stylus.rect_stylus import RectangleStylus
from .utils.misc import new_item_name


def replace_in_list(a_list, old, new):
    if old in a_list:
        a_list.remove(old)
    if new is not None:
        a_list.append(new)


class BackgroundArtist(BaseArtist):

    screen_bbox = Instance(BoundingBox)

    fill_color = Property

    stylus = Instance(RectangleStylus)

    def _set_fill_color(self, color):
        self.stylus.fill_color = color

    def _stylus_default(self):
        return RectangleStylus(edge_color='none')

    def draw(self, gc, view_bounds=None):
        self.stylus.draw(gc, self.screen_bbox.bounds)


class Canvas(Container):
    """ Represents a mapping from 2-D data space into 2-D screen space.

    It can house artists and other plot components, and otherwise behaves
    just like a normal Container.
    """

    bgcolor = config.get('background.canvas.color')

    #: Mapping of artist names to *lists* of artists.
    artists = Dict(Str, Instance(BaseArtist))

    # The bounding box containing data added this canvas.
    data_bbox = Instance(BoundingBox)

    #: Transform from data space to screen space.
    data_to_screen = Instance(BboxTransform)

    #: Transform from data space to screen space.
    screen_to_data = Property(Instance(BboxTransform),
                              depends_on='data_to_screen')

    #: Layout function which takes the container as the only argument.
    calculate_layout = Callable

    def _background_default(self):
        return BackgroundArtist(screen_bbox=self.screen_bbox,
                                fill_color=self.bgcolor)

    #--------------------------------------------------------------------------
    #  Public interface
    #--------------------------------------------------------------------------

    def add_artist(self, artist, name=None):
        if name is None:
            name = new_item_name(self.artists, name_template='artist_{}')

        self.data_bbox.update_from_extents(*artist.data_extents)
        artist.data_bbox = self.data_bbox
        self.artists[name] = artist
        self.add(artist)

    def replace_underlay(self, old, new):
        replace_in_list(self.underlays, old, new)

    def replace_overlay(self, old, new):
        replace_in_list(self.overlays, old, new)

    #--------------------------------------------------------------------------
    # Serialization interface
    #--------------------------------------------------------------------------

    def _iter_children(self):
        return self.artists.values()

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
        i.e. artists, fill the canvas.
        """
        self.calculate_layout(self)
