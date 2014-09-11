from __future__ import absolute_import

from abc import abstractmethod

from traits.api import ABCHasStrictTraits, Instance, Str, Tuple

from ..app.js.main import create_plot, show
from ..graph import Graph
from ..serialization.api import serialization_manager


WIDTH = 700
HEIGHT = 500


class JSWindow(ABCHasStrictTraits):
    """ A simple TraitsUI window for displaying a Graph """

    title = Str
    size = Tuple((WIDTH, HEIGHT))
    graph = Instance(Graph)

    @abstractmethod
    def setup_graph(self):
        """ Create `Graph` to display in the window. """

    def _graph_default(self):
        graph = self.setup_graph()
        graph.width = WIDTH
        graph.height = HEIGHT
        return graph

    def show(self):
        data = serialization_manager.serialize(self.graph)
        data['width'] = self.graph.width
        data['height'] = self.graph.height
        create_plot(data)
        show()
