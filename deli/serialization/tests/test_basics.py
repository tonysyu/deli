from deli.graph import Graph
from deli.serialization.api import serialize
from deli.testing.mock_window import MockWindow


class Demo(MockWindow):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Artist"
        return graph


def test_serialization():
    demo = Demo()
    output = serialize(demo.graph)

    assert output['__protocol__'] == 'Graph'

    canvas = output['canvas']
    assert canvas['__protocol__'] == 'Canvas'
