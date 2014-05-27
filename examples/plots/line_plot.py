from numpy import linspace
from scipy.special import jn

from deli.demo_utils import Window
from deli.graph import Graph
from deli.plots.line_plot import LinePlot


class Demo(Window):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Plot"

        x = linspace(-2.0, 10.0, 100)
        for i, color in enumerate(('red', 'green', 'blue')):
            y = jn(i, x)
            plot = LinePlot(x_data=x, y_data=y, color=color)
            graph.add_plot(plot)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
