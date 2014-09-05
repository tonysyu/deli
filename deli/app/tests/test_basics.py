import numpy as np

from deli.graph import Graph
from deli.plots.line_plot import LinePlot
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


def test_serialize():
    demo = Demo()
    output = demo.serialize()

    assert 'Graph' in output
    graph_attrs = output['Graph']

    assert 'Canvas' in graph_attrs
    canvas_attrs = graph_attrs['Canvas']

    assert 'LinePlot' in canvas_attrs