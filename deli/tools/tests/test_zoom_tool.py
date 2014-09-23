from numpy.testing import assert_allclose

from deli.testing.line_demo import LineDemo
from deli.tools.zoom_tool import ZoomTool


WIDTH = 100
HEIGHT = 200
X_MAX = 1
Y_MAX = 20


class Demo(LineDemo):

    size = (WIDTH, HEIGHT)
    init_x_limits = (0, X_MAX)
    init_y_limits = (0, Y_MAX)

    def _graph_default(self):
        graph = self.setup_graph()

        ZoomTool.attach_to(graph.canvas)
        return graph


def init_demo():
    demo = Demo()
    demo.show()
    return demo


def test_zoom_in():
    demo = init_demo()

    demo.control.press_release_key(character='+', x=0, y=0)

    expected_x_limits = (0.25 * X_MAX, 0.75 * X_MAX)
    expected_y_limits = (0.25 * Y_MAX, 0.75 * Y_MAX)
    assert_allclose(demo.x_limits, expected_x_limits)
    assert_allclose(demo.y_limits, expected_y_limits)


def test_zoom_out():
    demo = init_demo()

    demo.control.press_release_key(character='-', x=0, y=0)

    expected_x_limits = (-0.5 * X_MAX, 1.5 * X_MAX)
    expected_y_limits = (-0.5 * Y_MAX, 1.5 * Y_MAX)
    assert_allclose(demo.x_limits, expected_x_limits)
    assert_allclose(demo.y_limits, expected_y_limits)
