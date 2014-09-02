from numpy import linspace
from scipy.special import jn

from deli.demo_utils.traitsui import TraitsWindow
from deli.graph import Graph
from deli.plots.line_plot import LinePlot
from deli.style.colors import default_cycle


class Demo(TraitsWindow):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Plot"

        x = linspace(-2.0, 10.0, 100)
        for i in range(5):
            y = jn(i, x)
            plot = LinePlot(x_data=x, y_data=y, color=default_cycle.next())
            graph.add_plot(plot)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
