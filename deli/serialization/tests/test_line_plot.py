import numpy as np

from deli.graph import Graph
from deli.artist.line_artist import LineArtist
from deli.serialization.api import serialize
from deli.testing.mock_window import MockWindow


x = np.linspace(0, 10)
y = np.sin(x)


class Demo(MockWindow):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Artist"

        artist = LineArtist(x_data=x, y_data=y)
        graph.add_artist(artist)
        return graph


def test_draw():
    demo = Demo()
    demo.show()
    demo.context.begin_path.assert_called_with()
    demo.context.stroke_path.assert_called_with()
    demo.context.show_text.assert_called_with(demo.graph.title.text)


def test_serialization():
    demo = Demo()
    output = serialize(demo.graph.canvas)
    line_artist = output['artists'].values()[0]

    assert line_artist['__protocol__'] == 'LineArtist'
