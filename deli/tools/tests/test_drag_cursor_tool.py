import numpy as np

from traits.api import Instance

from deli.testing.line_demo import LineDemo
from deli.tools.data_cursor_tool import DataCursorTool


WIDTH = 10000
HEIGHT = 100
X_MAX = 100
Y_MAX = 10
# Make sure data points land on predictable points (round numbers)
N_POINTS = X_MAX + 1


class Demo(LineDemo):

    size = (WIDTH, HEIGHT)
    x = np.linspace(0, X_MAX, N_POINTS)
    y = np.linspace(0, Y_MAX, N_POINTS)

    tool = Instance(DataCursorTool)

    def _graph_default(self):
        graph = self.setup_graph()

        self.tool = DataCursorTool.attach_to(self.line_artist)
        return graph


def init_demo():
    demo = Demo()
    demo.show()
    return demo


def test_data_cursor_draw():
    demo = init_demo()
    demo.control.move_mouse(x=4200, y=0)
    data_point = demo.tool.overlay.data_point_to_string((42, 4.2))
    demo.context.show_text.assert_any_call(data_point)
