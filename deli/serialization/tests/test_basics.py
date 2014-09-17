from numpy.testing import assert_allclose

from deli.graph import Graph
from deli.serialization.api import serialize
from deli.testing.mock_window import MockWindow


class Demo(MockWindow):

    def __init__(self, **kwargs):
        super(Demo, self).__init__(**kwargs)
        self.do_layout()

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Artist"
        # We don't have data, so we'll get warnings if we don't set bounds.
        graph.canvas.data_bbox.rect = (0, 0, 1, 1)
        return graph


def test_setup():
    demo = Demo()
    assert all(w > 0 for w in demo.graph.size)
    assert all(w > 0 for w in demo.graph.canvas.size)


def test_serialization():
    demo = Demo()
    output = serialize(demo.graph)

    assert output['__protocol__'] == 'Graph'
    assert_allclose(output['size'], demo.graph.size)
    assert_allclose(output['origin'], demo.graph.origin)

    canvas = output['canvas']
    assert canvas['__protocol__'] == 'Canvas'
    assert_allclose(canvas['size'], demo.graph.canvas.size)
    assert_allclose(canvas['origin'], demo.graph.canvas.origin)
