from __future__ import absolute_import

import numpy as np
from kiva.basecore2d import GraphicsState

from vispy.util.transforms import ortho
from vispy import gloo

from . import markers


width = height = 512


def spiral():
    n = 500
    x0 = width / 2.0
    y0 = height / 2.0
    # Create radius that's within the bounds
    r = min(x0, y0) * 0.9
    theta = 0.0
    dtheta = 5.5 / 180.0 * np.pi

    xx, yy = [], []
    for i in range(n):
        theta += dtheta
        xx.append(x0 + r * np.cos(theta))
        yy.append(y0 + r * np.sin(theta))
        r -= 0.45
    return xx, yy


def gloo_program(data, fragments):
    vertex_buffer = gloo.VertexBuffer(data)

    view = np.eye(4, dtype=np.float32)
    model = np.eye(4, dtype=np.float32)
    projection = ortho(0, width, 0, height, -1, 1)
    program = gloo.Program(markers.vert, fragments)

    program.bind(vertex_buffer)
    program["u_antialias"] = 1
    program["u_size"] = 1
    program["u_model"] = model
    program["u_view"] = view
    program["u_projection"] = projection

    return program


def marker_program(x, y, marker='disc', line_width=1, size=5,
                   fg_color=(0, 0, 0, 1), bg_color=(1, 1, 1, 1)):
    assert len(x) == len(y)

    positions = np.transpose([x, y, np.zeros_like(x)])

    n = len(x)
    data = np.zeros(n, dtype=[('a_position', np.float32, 3),
                              ('a_fg_color', np.float32, 4),
                              ('a_bg_color', np.float32, 4),
                              ('a_size', np.float32, 1),
                              ('a_linewidth', np.float32, 1)])
    data['a_position'] = positions
    data['a_size'] = size
    data['a_fg_color'] = fg_color
    data['a_bg_color'] = bg_color
    data['a_linewidth'] = line_width

    fragments = markers.frag + markers.MARKER[marker]
    return data, fragments


class GraphicsContext(object):

    def __init__(self):
        self._gloo_programs = []
        self._state = GraphicsState()
        self._state_stack = [self._state]

    def render(self, event):
        for program in self._gloo_programs:
            program.draw('points')

    def clear(self, *args):
        pass

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

    def translate_ctm(self, dx, dy):
        pass

    def rotate_ctm(self, radian_angle):
        pass

    def set_font(self, font):
        pass

    def set_text_position(self, x, y):
        pass

    def get_full_text_extent(self, text):
        return 1, 1, 0, 0

    def show_text(self, text):
        pass

    def set_antialias(self, state):
        pass

    def set_alpha(self, alpha):
        pass

    def set_stroke_color(self, color):
        pass

    def set_fill_color(self, color):
        self._state.fill_color = color

    def set_line_width(self, width):
        pass

    def set_line_dash(self, style):
        pass

    def lines(self, points):
        pass

    def line_set(self, starts, ends):
        pass

    def begin_path(self):
        pass

    def stroke_path(self):
        pass

    def fill_path(self):
        pass

    def draw_marker_at_points(self, points, size=5, marker='disc'):
        data, fragments = marker_program(*np.transpose(points), size=size,
                                         bg_color=self._state.fill_color)
        self._gloo_programs.append(gloo_program(data, fragments))

    def draw_rect(self, rect):
        pass

    def clip_to_rect(self, *rect):
        pass
