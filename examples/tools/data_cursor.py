import numpy as np

from deli.demo_utils import Window
from deli.plot_canvas import PlotCanvas
from deli.tools.data_cursor_tool import DataCursorTool
from deli.utils.data_structures import NoisyDict


class Demo(Window):

    def setup_canvas(self):
        x = np.linspace(0, 2 * np.pi)
        pd = NoisyDict(x=x, y1=np.sin(x), y2=np.cos(x))

        canvas = PlotCanvas(data=pd)
        canvas.title.text = "Line Plot"

        for y_name, color in zip(('y1', 'y2'), ('black', 'red')):
            renderer = canvas.plot(('x', y_name), color=color)[0]
            DataCursorTool.attach_to(renderer)

        return canvas


if __name__ == '__main__':
    demo = Demo()
    demo.configure_traits()
