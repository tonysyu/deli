import numpy as np

from deli.array_data_source import ArrayDataSource
from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.renderer.marker_renderer import MarkerRenderer
from deli.utils.data_structures import NoisyDict


class Demo(Window):

    def setup_canvas(self):
        x = np.linspace(-2.0, 10.0, 100)
        y = np.sin(x)
        pd = NoisyDict(x=x, y=y)

        canvas = PlotCanvas(data=pd)
        canvas.title.text = "Scatter Plot"
        canvas.data_bbox.bounds = (x.min(), y.min(), x.ptp(), y.ptp())

        x_src = ArrayDataSource(x)
        y_src = ArrayDataSource(y)
        renderer = MarkerRenderer(x_src=x_src, y_src=y_src,
                                  data_bbox=canvas.data_bbox)
        canvas.add(renderer)
        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
