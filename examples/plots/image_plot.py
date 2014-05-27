from skimage import data

from deli.demo_utils import Window
from deli.graph import Graph
from deli.plots.image_plot import ImagePlot


class Demo(Window):

    def setup_graph(self):
        graph = Graph()
        plot = ImagePlot(data=data.lena())
        graph.add_plot(plot)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
