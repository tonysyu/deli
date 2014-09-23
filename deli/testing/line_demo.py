import numpy as np

from traits.api import Tuple

from deli.graph import Graph
from deli.artist.line_artist import LineArtist
from deli.testing.mock_view import MockView


class LineDemo(MockView):

    init_x_limits = Tuple((1, 2))
    init_y_limits = Tuple((10, 20))

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Artist"

        x = np.linspace(*self.init_x_limits)
        y = np.linspace(*self.init_y_limits)
        artist = LineArtist(x_data=x, y_data=y)
        graph.add_artist(artist)
        return graph
