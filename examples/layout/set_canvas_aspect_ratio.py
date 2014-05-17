import numpy as np

from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.plots.line_plot import LinePlot


class Demo(Window):

    def setup_canvas(self):
        canvas = PlotCanvas()
        canvas.title.text = "Line Plot"
        canvas.aspect_ratio = 1

        x = np.linspace(-2.0, 10.0, 100)
        plot = LinePlot(x_data=x, y_data=np.sin(x))
        canvas.add(plot)
        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
