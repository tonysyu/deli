from deli.app import backend
backend.use('testing.mock')

from deli.graph import Graph
from deli.testing.mock_view import MockView


class Demo(MockView):

    def __init__(self, **kwargs):
        super(Demo, self).__init__(**kwargs)
        self.do_layout()

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Artist"
        # We don't have data, so we'll get warnings if we don't set bounds.
        graph.canvas.data_bbox.rect = (0, 0, 1, 1)
        return graph


demo = Demo()
demo.show()
