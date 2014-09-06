import numpy as np

from deli.graph import Graph
from deli.plots.line_plot import LinePlot
from deli.serialization.api import serialize
from deli.testing.mock_window import MockWindow


x = np.linspace(0, 10)
y = np.sin(x)


class Demo(MockWindow):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Plot"

        plot = LinePlot(x_data=x, y_data=y)
        graph.add_plot(plot)
        return graph


def test_draw():
    demo = Demo()
    demo.show()
    demo.context.begin_path.assert_called_with()
    demo.context.stroke_path.assert_called_with()
    demo.context.show_text.assert_called_with(demo.graph.title.text)


def test_serialization():
    demo = Demo()
    output = serialize(demo.graph)

    assert output['__protocol__'] == 'Graph'

    canvas = output['canvas']
    assert canvas['__protocol__'] == 'Canvas'

    plots = canvas['plots'].values()
    assert plots[0]['__protocol__'] == 'LinePlot'
