import numpy as np

from traits.api import Any, Instance, cached_property

from deli.artist.base_point_artist import BasePointArtist
from deli.axis import XAxis
from deli.demo_utils.traits_view import TraitsView
from deli.graph import Graph
from deli.layout.grid_layout import XGridLayout
from deli.stylus.rect_stylus import RectangleStylus
from deli.utils.drawing import broadcast_points

ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class TickLayout(XGridLayout):

    @cached_property
    def _get_axial_offsets(self):
        return np.arange(*np.ceil(self.axial_limits))


class OrdinalAxis(XAxis):

    labels = Any

    def _tick_grid_default(self):
        return TickLayout(data_bbox=self.component.data_bbox)

    def data_offset_to_label(self, data_offset):
        index = int(data_offset)
        if 0 <= index < len(self.labels):
            return self.labels[index]
        return ''


def line_to_rect_corners(x, y0, y1, width):
    half_width = width / 2.0
    corner0 = broadcast_points(x - half_width, y0)
    corner1 = broadcast_points(x + half_width, y1)
    return corner0, corner1


def bars_from_points(x, y, data_to_screen, y0=0, width=None):
    if width is None:
        width = np.min(np.diff(x))

    corner0, corner1 = line_to_rect_corners(x, y0, y, width)

    origins = data_to_screen.transform(corner0)
    sizes = data_to_screen.transform(corner1) - origins
    return np.hstack([origins, sizes])


class BarArtist(BasePointArtist):
    """ An artist for bar plot data. """

    stylus = Instance(RectangleStylus, ())

    def draw(self, gc, view_rect=None):
        bars = self.get_bar_data()
        with self._clipped_context(gc):
            for rect in bars:
                self.stylus.draw(gc, rect)

    def get_bar_data(self):
        x, y = self.x_data, self.y_data
        return bars_from_points(x, y, self.data_to_screen, width=0.5)

class Demo(TraitsView):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Bar Artist"
        graph.x_axis = OrdinalAxis(component=graph.canvas, labels=ALPHA[:10])

        x = np.arange(10)
        artist = BarArtist(x_data=x, y_data=np.cos(x))
        graph.add_artist(artist)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
