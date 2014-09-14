import numpy as np

from traits.api import Any, DelegatesTo, Instance

from deli.stylus.rect_stylus import RectangleStylus
from deli.axis import XAxis
from deli.demo_utils.traitsui import TraitsWindow
from deli.graph import Graph
from deli.artist.base_point_artist import BasePointArtist


ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class OrdinalAxis(XAxis):

    labels = Any

    def data_offset_to_label(self, data_offset):
        index = int(data_offset)
        if 0 <= index < len(self.labels):
            return self.labels[index]
        return ''


class BarArtist(BasePointArtist):
    """ A plot for line data.
    """

    stylus = Instance(RectangleStylus, ())

    #--------------------------------------------------------------------------
    #  Private interface
    #--------------------------------------------------------------------------

    def _render(self, gc, points, selected_points=None):
        x0, y0 = self.data_to_screen.transform([0, 0])
        with gc:
            gc.clip_to_rect(*self.screen_bbox.rect)
            # self.stylus.update_style(gc)
            width = 20
            for x, y in points:
                rect = (x-width/2.0, y0, width, y - y0)
                self.stylus.draw(gc, rect)


class Demo(TraitsWindow):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Bar Artist"
        graph.x_axis = OrdinalAxis(component=graph.canvas,
                                   labels=ALPHA[:10])

        x = np.arange(10)
        artist = BarArtist(x_data=x, y_data=np.sin(x))
        graph.add_artist(artist)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
