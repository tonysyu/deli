from numpy import linspace
from scipy.special import jn

from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.plots.line_plot import LinePlot


class Demo(Window):

    def setup_canvas(self):
        canvas = PlotCanvas()
        canvas.title.text = "Line Plot"

        x = linspace(-2.0, 10.0, 100)
        for i, color in enumerate(('red', 'green', 'blue')):
            y = jn(i, x)
            plot = LinePlot(x_data=x, y_data=y, color=color)
            canvas.add(plot)
        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
