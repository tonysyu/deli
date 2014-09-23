from numpy.testing import assert_allclose

from traits.api import Property

from deli.testing.line_demo import LineDemo
from deli.tools.pan_tool import PanTool


WIDTH = 100
HEIGHT = 200
X_MAX = 1
Y_MAX = 20


class Demo(LineDemo):

    size = (WIDTH, HEIGHT)
    init_x_limits = (0, X_MAX)
    init_y_limits = (0, Y_MAX)

    x_limits = Property
    y_limits = Property

    def _get_x_limits(self):
        return self.graph.canvas.data_bbox.x_limits

    def _get_y_limits(self):
        return self.graph.canvas.data_bbox.y_limits

    def _graph_default(self):
        graph = self.setup_graph()
        graph.margin = 0

        PanTool.attach_to(graph.canvas)
        return graph


def init_demo():
    demo = Demo()
    demo.show()
    return demo


def test_pan_x():
    demo = init_demo()
    original_x_limits = demo.x_limits
    # Dragging by half the canvas width moves the x-bounds by half the x-range.
    demo.control.press_move_release(x=(0, WIDTH/2), y=HEIGHT/2)
    assert_allclose(demo.x_limits, original_x_limits - X_MAX/2.0)


def test_pan_y():
    demo = init_demo()
    original_y_limits = demo.y_limits
    # Dragging by half the canvas width moves the y-bounds by half the y-range.
    demo.control.press_move_release(x=WIDTH/2, y=(0, HEIGHT/2))
    assert_allclose(demo.y_limits, original_y_limits - Y_MAX/2.0)
