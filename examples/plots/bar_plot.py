import numpy as np

from traits.api import Any, cached_property

from deli.artist.vbar_artist import VBarArtist
from deli.axis import XAxis
from deli.demo_utils.traits_view import TraitsView
from deli.graph import Graph
from deli.layout.grid_layout import XGridLayout

ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class FixedTickLayout(XGridLayout):

    ticks = Any

    @cached_property
    def _get_axial_offsets(self):
        x_min, x_max = self.axial_limits
        return self.ticks[(self.ticks >= x_min) & (self.ticks <= x_max)]


class OrdinalAxis(XAxis):

    labels = Any

    def _tick_grid_default(self):
        ticks = np.arange(len(self.labels))
        return FixedTickLayout(data_bbox=self.data_bbox, ticks=ticks)

    def data_offset_to_label(self, data_offset):
        index = int(data_offset)
        if 0 <= index < len(self.labels):
            return self.labels[index]
        return ''


class Demo(TraitsView):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Bar Artist"
        graph.x_axis = OrdinalAxis(labels=ALPHA[:10])

        x = np.arange(10)
        artist = VBarArtist(x_data=x, y_data=np.cos(x))
        graph.add_artist(artist)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
