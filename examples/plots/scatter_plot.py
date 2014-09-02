import numpy as np

from deli.demo_utils.traitsui import TraitsWindow
from deli.graph import Graph
from deli.plots.scatter_plot import ScatterPlot


class Demo(TraitsWindow):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Scatter Plot"

        x = np.linspace(-2.0, 10.0, 100)
        plot = ScatterPlot(x_data=x, y_data=np.sin(x))

        graph.add_plot(plot)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
