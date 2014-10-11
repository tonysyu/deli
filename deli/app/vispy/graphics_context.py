from __future__ import absolute_import

import numpy as np
from kiva.basecore2d import GraphicsState

from vispy import gloo
from vispy.util.transforms import ortho

from . import lines
from . import markers


identity_transform = np.eye(4, dtype=np.float32)


def create_program(data, vert_shader, fragments):

    program = gloo.Program(vert_shader, fragments)

    vertex_buffer = gloo.VertexBuffer(data)
    program.bind(vertex_buffer)

    view = model = identity_transform
    program["u_antialias"] = 1
    program["u_size"] = 1
    program["u_model"] = model
    program["u_view"] = view
    return program


class GraphicsContext(object):

    def __init__(self, size):
        gloo.set_viewport(0, 0, *size)

        self._size = size
        self._gloo_programs = []
        self._state = GraphicsState()
        self._state.ctm = (0, 0)
        self._state_stack = [self._state]

    def render(self, event):
        for program in self._gloo_programs:
            # XXX: Define custom draw commands to remove having to call both.
            program.draw('points')
            program.draw('line_strip')
        self._gloo_programs = []

    def clear(self, *args):
        pass

    def __enter__(self):
        # Set new state to copy of present state (which can be modified.
        self._state = self._state.copy()
        self._state_stack.append(self._state)

    def __exit__(self, type, value, traceback):
        self._state = self._state_stack.pop()

    def translate_ctm(self, dx, dy):
        # XXX: This is just a hack to fake offsets
        x, y = self._state.ctm
        self._state.ctm = (x+dx, y+dy)

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

    def set_antialias(self, antialias):
        self._state.antialias = antialias

    def set_alpha(self, alpha):
        self._state.line_color = alpha

    def set_stroke_color(self, color):
        self._state.line_color = color

    def set_fill_color(self, color):
        self._state.fill_color = color

    def set_line_width(self, width):
        self._state.line_width = width

    def set_line_dash(self, dash):
        self._state.line_dash = dash

    def lines(self, points):
        self._points.append(points)

    def line_set(self, starts, ends):
        # self._points.append(np.vstack([starts, ends]))
        pass

    def begin_path(self):
        self._points = []

    def stroke_path(self):
        if len(self._points) == 0:
            return
        points = np.vstack(self._points)
        data, fragments = lines.data(points,
                                     color=self._state.line_color,
                                     line_width=self._state.line_width)
        program = create_program(data, lines.vert_shader, fragments)
        program['u_projection'] = self._get_projection()
        self._gloo_programs.append(program)
        self._points = []

    def fill_path(self):
        pass

    def draw_marker_at_points(self, points, size=5, marker='disc'):
        data, fragments = markers.data(points, size=size,
                                       bg_color=self._state.fill_color)
        program = create_program(data, markers.vert_shader, fragments)
        program['u_projection'] = self._get_projection()
        self._gloo_programs.append(program)

    def draw_rect(self, rect):
        pass

    def clip_to_rect(self, *rect):
        pass

    def _get_projection(self):
        x, y = self._state.ctm
        width, height = self._size
        return ortho(-x, width, -y, height, -1, 1)
