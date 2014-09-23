import numpy as np

from traits.api import Tuple, Property

from deli.graph import Graph
from deli.artist.line_artist import LineArtist
from deli.testing.mock_view import MockView


class LineDemo(MockView):
    """ Mock view of plot with a simple line artist.

    This demo view sets the graph margin to zero, so that the view size matches
    the canvas size exactly. You can set the initial data limits of this view
    (`init_x_limits` and `init_y_limits`) intelligently to give a simple
    conversion between screen and data coordinates.
    """

    init_x_limits = Tuple((1, 2))
    init_y_limits = Tuple((10, 20))

    x_limits = Property
    y_limits = Property

    def _get_x_limits(self):
        return self.graph.canvas.data_bbox.x_limits

    def _get_y_limits(self):
        return self.graph.canvas.data_bbox.y_limits

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Artist"

        x = np.linspace(*self.init_x_limits)
        y = np.linspace(*self.init_y_limits)
        artist = LineArtist(x_data=x, y_data=y)
        graph.add_artist(artist)

        graph.margin = 0
        return graph
