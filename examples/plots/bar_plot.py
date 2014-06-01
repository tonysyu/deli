import numpy as np

from traits.api import Any

from deli.axis import XAxis
from deli.demo_utils.traitsui import TraitsWindow
from deli.graph import Graph
from deli.plots.line_plot import LinePlot


ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class OrdinalAxis(XAxis):

    labels = Any

    def data_offset_to_label(self, data_offset):
        index = int(data_offset)
        if 0 <= index < len(self.labels):
            return self.labels[index]
        return ''


class Demo(TraitsWindow):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Bar Plot (not really)"
        graph.x_axis = OrdinalAxis(component=graph.canvas,
                                   labels=ALPHA[:10])

        x = np.arange(10)
        plot = LinePlot(x_data=x, y_data=np.sin(x))
        graph.add_plot(plot)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
