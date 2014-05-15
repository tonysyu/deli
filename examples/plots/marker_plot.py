import numpy as np

from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.renderer.marker_renderer import MarkerRenderer


class Demo(Window):

    def setup_canvas(self):
        canvas = PlotCanvas()
        canvas.title.text = "Scatter Plot"

        x = np.linspace(-2.0, 10.0, 100)
        renderer = MarkerRenderer(x_data=x, y_data=np.sin(x))

        canvas.add(renderer)
        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
