import numpy as np

from traits.api import Instance

from deli.demo_utils.traits_view import FigureView
from deli.graph import Graph
from deli.artist.line_artist import LineArtist
from deli.artist.scatter_artist import ScatterArtist


class Demo(FigureView):

    line_graph = Instance(Graph)
    scatter_graph = Instance(Graph)

    def _line_graph_default(self):
        graph = Graph()
        graph.title.text = "Line Artist"

        x = np.linspace(0, 10.0, 100)
        artist = LineArtist(x_data=x, y_data=np.sin(x))
        graph.add_artist(artist)
        return graph

    def _scatter_graph_default(self):
        graph = Graph()
        graph.title.text = "Scatter Artist"

        x = np.linspace(0, 10.0, 100)
        artist = ScatterArtist(x_data=x, y_data=np.sin(x))
        graph.add_artist(artist)
        return graph

    def create_graphs(self):
        return self.line_graph, self.scatter_graph


if __name__ == "__main__":
    demo = Demo()
    demo.show()
