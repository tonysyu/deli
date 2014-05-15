import numpy as np

from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.plots.line_plot import LinePlot
from deli.tools.data_cursor_tool import DataCursorTool


class Demo(Window):

    def setup_canvas(self):
        x = np.linspace(0, 2 * np.pi)
        y1 = np.sin(x)
        y2 = np.cos(x)

        canvas = PlotCanvas()
        canvas.title.text = "Data cursor"

        for y, color in zip((y1, y2), ('black', 'red')):
            plot = LinePlot(x_data=x, y_data=y, color=color)
            canvas.add(plot)
            DataCursorTool.attach_to(plot)

        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
