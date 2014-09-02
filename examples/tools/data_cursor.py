import numpy as np

from deli.demo_utils.traitsui import TraitsWindow
from deli.graph import Graph
from deli.plots.line_plot import LinePlot
from deli.tools.data_cursor_tool import DataCursorTool


class Demo(TraitsWindow):

    def setup_graph(self):
        x = np.linspace(0, 2 * np.pi)
        y1 = np.sin(x)
        y2 = np.cos(x)

        graph = Graph()
        graph.title.text = "Data cursor"

        for y, color in zip((y1, y2), ('black', 'red')):
            plot = LinePlot(x_data=x, y_data=y, color=color)
            graph.add_plot(plot)
            DataCursorTool.attach_to(plot)

        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
