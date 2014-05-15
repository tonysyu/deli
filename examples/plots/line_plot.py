from numpy import linspace
from scipy.special import jn

from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.renderer.line_renderer import LineRenderer


class Demo(Window):

    def setup_canvas(self):
        canvas = PlotCanvas()
        canvas.title.text = "Line Plot"

        x = linspace(-2.0, 10.0, 100)
        for i, color in enumerate(('red', 'green', 'blue')):
            y = jn(i, x)
            renderer = LineRenderer(x_data=x, y_data=y, color=color)
            canvas.add(renderer)
        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
