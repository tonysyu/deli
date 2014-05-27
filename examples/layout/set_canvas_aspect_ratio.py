import numpy as np

from deli.demo_utils import Window
from deli.graph import Graph
from deli.plots.line_plot import LinePlot


class Demo(Window):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Plot"
        graph.aspect_ratio = 1

        x = np.linspace(-2.0, 10.0, 100)
        plot = LinePlot(x_data=x, y_data=np.sin(x))
        graph.add_plot(plot)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
