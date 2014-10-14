import numpy as np

import OpenGL.GL as GL

from .element import GLElement, create_program


class LineElement(GLElement):

    def __init__(self, points, state, segments=False):
        super(LineElement, self).__init__(state)

        self._line_width =  state.line_width
        data = create_data(np.vstack(points), color=state.line_color)
        self._program = create_program(data, VERT_SHADER, FRAG_SHADER)

        self._draw_as_segments = segments

    def draw(self):
        with self._draw_context():
            GL.glLineWidth(self._line_width)
            GL.glEnable(GL.GL_LINE_SMOOTH)
            if self._draw_as_segments:
                self._program.draw('lines')
            else:
                self._program.draw('line_strip')
            GL.glDisable(GL.GL_LINE_SMOOTH)


def create_data(points, line_width=3, color=(0, 0, 0, 1)):
    """ Return data and fragment shader for markers. """
    x, y = np.transpose(points)
    positions = np.transpose([x, y, np.zeros_like(x)])

    n = len(x)
    data = np.zeros(n, dtype=[('a_position', np.float32, 3),
                              ('a_color', np.float32, 4),
                              ('a_linewidth', np.float32, 1)])
    data['a_position'] = positions
    data['a_color'] = color
    data['a_linewidth'] = line_width
    return data


VERT_SHADER = """
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_antialias;
uniform float u_size;

attribute vec3 a_position;
attribute vec4  a_color;
attribute float a_linewidth;

varying float v_id;
varying vec4 v_color;
varying float v_linewidth;
varying float v_antialias;

void main (void) {
    v_color  = a_color;
    v_antialias = u_antialias;
    v_linewidth = a_linewidth;

    gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
}
"""

FRAG_SHADER = """
varying float v_id;
varying vec4 v_color;

void main()
{
    gl_FragColor = v_color;
}
"""
