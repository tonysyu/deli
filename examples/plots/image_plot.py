from skimage import data

from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.plots.image_plot import ImagePlot


class Demo(Window):

    def setup_canvas(self):
        canvas = PlotCanvas()
        plot = ImagePlot(data=data.lena())
        canvas.add(plot)
        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
