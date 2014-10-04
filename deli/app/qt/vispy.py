from __future__ import absolute_import

import numpy as np

from traits.api import Instance

from vispy.util.transforms import ortho
from vispy import gloo

from .base_window import BaseWindow
from .qgl_backend import QGLBackend

from . import vispy_markers


width = height = 512

n = 500
data = np.zeros(n, dtype=[('a_position', np.float32, 3),
                          ('a_fg_color', np.float32, 4),
                          ('a_bg_color', np.float32, 4),
                          ('a_size', np.float32, 1),
                          ('a_linewidth', np.float32, 1)])
data['a_fg_color'] = 0, 0, 0, 1
data['a_bg_color'] = 1, 1, 1, 1
data['a_linewidth'] = 1

radius, theta, dtheta = 255.0, 0.0, 5.5 / 180.0 * np.pi
for i in range(n):
    theta += dtheta
    x = 256 + radius * np.cos(theta)
    y = 256 + radius * np.sin(theta)
    r = 10.1 - i * 0.02
    radius -= 0.45
    data['a_position'][i] = x, y, 0
    data['a_size'][i] = 2 * r


class GraphicsContext(object):

    def __init__(self):
        vbo = gloo.VertexBuffer(data)
        view = np.eye(4, dtype=np.float32)
        model = np.eye(4, dtype=np.float32)
        projection = ortho(0, width, 0, height, -1, 1)
        marker_fragments = vispy_markers.frag + vispy_markers.ring
        program = gloo.Program(vispy_markers.vert, marker_fragments)

        program.bind(vbo)
        program["u_antialias"] = 1
        program["u_size"] = 1
        program["u_model"] = model
        program["u_view"] = view
        program["u_projection"] = projection

        self._vispy_program = program

    def render(self, event):
        self._vispy_program.draw('points')

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
        pass

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

    def draw_rect(self, rect):
        pass

    def clip_to_rect(self, *rect):
        pass


class Window(BaseWindow):

    _gc = Instance(GraphicsContext)

    control = Instance(QGLBackend)

    def _create_control(self, parent, proxy_window):
        """ Create the toolkit control. """
        return QGLBackend(parent, proxy_window)

    def _create_gc(self, size, pix_format="bgra32"):
        self._gc = GraphicsContext()
        return self._gc

    def _render(self, event):
        gloo.clear()
        if self.control is None:
            return
        self._gc.render(event)
        self.control.swapBuffers()
