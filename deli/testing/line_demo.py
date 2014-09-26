import numpy as np

from traits.api import Any, Instance, Property

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

    # XXX: `x`/`y` fail weirdly if defined as an Array trait and subclass sets
    # directly to numpy arrays.
    x = Any(np.linspace(1, 2))
    y = Any(np.linspace(10, 20))

    x_limits = Property
    y_limits = Property

    line_artist = Instance(LineArtist)

    def _get_x_limits(self):
        return self.graph.canvas.data_bbox.x_limits

    def _get_y_limits(self):
        return self.graph.canvas.data_bbox.y_limits

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Artist"

        self.line_artist = LineArtist(x_data=self.x, y_data=self.y)
        graph.add_artist(self.line_artist)

        graph.margin = 0
        return graph
