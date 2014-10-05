import numpy as np

from deli.demo_utils.traits_view import TraitsView
from deli.graph import Graph
from deli.artist.marker_artist import MarkerArtist


class Demo(TraitsView):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Scatter Artist"

        x = np.linspace(-2.0, 10.0, 100)
        artist = MarkerArtist(x_data=x, y_data=np.sin(x))

        graph.add_artist(artist)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
