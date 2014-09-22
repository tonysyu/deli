from __future__ import absolute_import

from abc import abstractmethod

from mock import MagicMock

from traits.api import (ABCHasStrictTraits, DelegatesTo, Instance, Property,
                        Str, Tuple)

from ..graph import Graph
from ..app.testing.mock_window import MockWindow


WIDTH = 700
HEIGHT = 500


def calculate_text_extent(text):
    width = len(text)
    height = 1
    leading = descent = 0
    return width, height, descent, leading


class MockView(ABCHasStrictTraits):

    title = Str
    graph = Instance(Graph)
    context = Property

    size = Tuple((WIDTH, HEIGHT))
    origin = Tuple((0, 0))
    rect = Property

    _window = Instance(MockWindow)
    control = DelegatesTo('_window')

    @abstractmethod
    def setup_graph(self):
        """ Create `Graph` to display in the window. """

    def _graph_default(self):
        return self.setup_graph()

    def __window_default(self):
        return MockWindow(component=self.graph)

    def _get_context(self):
        return self._window._gc

    def _get_rect(self):
        return self.origin + self.size

    def do_layout(self):
        self.setup_graph()
        self.graph.origin = self.origin
        self.graph.size = self.size

    def show(self):
        self.do_layout()
        self._window.render()
