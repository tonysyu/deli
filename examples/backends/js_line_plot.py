import numpy as np

from deli.demo_utils.js_view import JSView
from deli.graph import Graph
from deli.artist.line_artist import LineArtist


class Demo(JSView):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Artist"

        x = np.linspace(0, 10)
        y = np.sin(x)
        artist = LineArtist(x_data=x, y_data=y)
        graph.add_artist(artist)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
