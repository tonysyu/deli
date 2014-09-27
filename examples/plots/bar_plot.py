import numpy as np

from traits.api import Any, cached_property

from deli.artist.hbar_artist import HBarArtist
from deli.artist.vbar_artist import VBarArtist
from deli.axis import XAxis, YAxis
from deli.demo_utils.traits_view import FigureView
from deli.graph import Graph
from deli.layout.grid_layout import XGridLayout, YGridLayout

ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def create_ordinal_axis(axis_class, grid_class):

    class FixedTickLayout(grid_class):

        ticks = Any

        @cached_property
        def _get_axial_offsets(self):
            x_min, x_max = self.axial_limits
            return self.ticks[(self.ticks >= x_min) & (self.ticks <= x_max)]

    class OrdinalAxis(axis_class):

        labels = Any

        def _tick_grid_default(self):
            ticks = np.arange(len(self.labels))
            return FixedTickLayout(data_bbox=self.data_bbox, ticks=ticks)

        def data_offset_to_label(self, data_offset):
            index = int(data_offset)
            if 0 <= index < len(self.labels):
                return self.labels[index]
            return ''

    return OrdinalAxis


OrdinalXAxis = create_ordinal_axis(XAxis, XGridLayout)
OrdinalYAxis = create_ordinal_axis(YAxis, YGridLayout)


class Demo(FigureView):

    size = (500, 800)

    def create_vbar_graph(self):
        graph = Graph()
        graph.title.text = "Vertical Bars"
        graph.x_axis = OrdinalXAxis(labels=ALPHA[:10])

        x = np.arange(10)
        graph.add_artist(VBarArtist(x_data=x, y_data=np.cos(x)))
        return graph

    def create_hbar_graph(self):
        graph = Graph()
        graph.title.text = "Horizontal Bars"
        graph.y_axis = OrdinalYAxis(labels=ALPHA[:8])

        y = np.arange(8)
        graph.add_artist(HBarArtist(x_data=np.cos(y), y_data=y))
        return graph

    def create_graphs(self):
        return self.create_vbar_graph(), self.create_hbar_graph()


if __name__ == '__main__':
    demo = Demo()
    demo.show()
