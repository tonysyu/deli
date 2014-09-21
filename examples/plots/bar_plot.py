import numpy as np

from traits.api import Any, Instance

from deli.stylus.rect_stylus import RectangleStylus
from deli.axis import XAxis
from deli.demo_utils.traitsui import TraitsWindow
from deli.graph import Graph
from deli.artist.base_point_artist import BasePointArtist
from deli.utils.drawing import broadcast_points

ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class OrdinalAxis(XAxis):

    labels = Any

    def data_offset_to_label(self, data_offset):
        index = int(data_offset)
        if 0 <= index < len(self.labels):
            return self.labels[index]
        return ''


class BarArtist(BasePointArtist):
    """ An artist for bar plot data. """

    stylus = Instance(RectangleStylus, ())

    def draw(self, gc, view_rect=None):
        bars = self._bars_from_points(width=0.5)
        with self._clipped_context(gc):
            for rect in bars:
                self.stylus.draw(gc, rect)

    # -------------------------------------------------------------------------
    #  Private interface
    # -------------------------------------------------------------------------

    def _bars_from_points(self, width=None, y0=0):
        x = self.x_data
        y = self.y_data

        if width is None:
            width = np.min(np.diff(x))

        corner0 = broadcast_points(x - (width / 2.0), y0)
        corner1 = broadcast_points(x + (width / 2.0), y)

        origins = self.data_to_screen.transform(corner0)
        sizes = self.data_to_screen.transform(corner1) - origins
        return np.hstack([origins, sizes])


class Demo(TraitsWindow):

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
