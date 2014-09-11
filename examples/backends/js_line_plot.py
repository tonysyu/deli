import numpy as np

from deli.demo_utils.js_widget import JSWindow
from deli.graph import Graph
from deli.plots.line_plot import LinePlot


class Demo(JSWindow):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Plot"

        x = np.linspace(0, 10)
        y = np.sin(x)
        plot = LinePlot(x_data=x, y_data=y)
        graph.add_plot(plot)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
