import numpy as np

from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.renderer.line_renderer import LineRenderer
from deli.tools.data_cursor_tool import DataCursorTool


class Demo(Window):

    def setup_canvas(self):
        x = np.linspace(0, 2 * np.pi)
        y1 = np.sin(x)
        y2 = np.cos(x)

        canvas = PlotCanvas()
        canvas.title.text = "Data cursor"

        for y, color in zip((y1, y2), ('black', 'red')):
            renderer = LineRenderer(x_data=x, y_data=y, color=color)
            canvas.add(renderer)
            DataCursorTool.attach_to(renderer)

        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
