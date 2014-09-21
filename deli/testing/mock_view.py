from __future__ import absolute_import

from abc import abstractmethod

from mock import MagicMock

from traits.api import ABCHasStrictTraits, Instance, Property, Str, Tuple

from ..graph import Graph


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
    context = Instance(MagicMock)

    size = Tuple((WIDTH, HEIGHT))
    origin = Tuple((0, 0))
    rect = Property

    @abstractmethod
    def setup_graph(self):
        """ Create `Graph` to display in the window. """

    def _graph_default(self):
        return self.setup_graph()

    def _context_default(self):
        context = MagicMock()

        context.get_full_text_extent.side_effect = calculate_text_extent
        return context

    def _get_rect(self):
        return self.origin + self.size

    def do_layout(self):
        self.setup_graph()
        self.graph.origin = self.origin
        self.graph.size = self.size

    def show(self):
        self.do_layout()
        self.graph.render(self.context, view_rect=self.rect)
