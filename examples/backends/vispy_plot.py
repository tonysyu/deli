import numpy as np

from deli.app import backend
backend.use('qt.vispy')

from deli.demo_utils.traits_view import TraitsView
from deli.graph import Graph
from deli.artist.line_artist import LineArtist
from deli.artist.marker_artist import MarkerArtist


class Demo(TraitsView):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Artist"

        x = np.linspace(-2.0, 10.0, 100)
        artist = LineArtist(x_data=x, y_data=np.sin(x), color='gray')
        artist.line.width = 2

        graph.add_artist(artist)
        artist = MarkerArtist(x_data=x, y_data=np.sin(x))
        graph.add_artist(artist)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
