"""
Rectangular element in vispy.
"""
import numpy as np

import OpenGL.GL as GL

from .element import GLElement, set_program_data


class RectElement(GLElement):

    def __init__(self):
        super(RectElement, self).__init__(VERT_SHADER, FRAG_SHADER)

    def update(self, state, rect):
        super(RectElement, self).update(state)

        self._fill_color = state.fill_color
        self._edge_color = state.line_color

        data = create_data(rect)
        set_program_data(self._program, data)

    def draw(self):
        self._program['u_color'] = self._fill_color
        self._program.draw('triangle_strip')

        GL.glEnable(GL.GL_LINE_SMOOTH)
        self._program['u_color'] = self._edge_color
        self._program.draw('line_strip')
        GL.glDisable(GL.GL_LINE_SMOOTH)


def create_data(rect):
    """ Return data and fragment shader for markers. """
    x0, y0, width, height = rect
    x1, y1 = x0 + width, y0 + height
    points = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    positions = np.hstack([points, np.zeros((len(points), 1))])

    data = np.zeros(len(positions), dtype=[('a_position', np.float32, 3)])
    data['a_position'] = positions
    return data


VERT_SHADER = """
#version 120

// Uniforms
// ------------------------------------
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_antialias;
uniform float u_size;
uniform vec4 u_color;

// Attributes
// ------------------------------------
attribute vec3  a_position;

// Varyings
// ------------------------------------
varying vec4 v_color;

void main (void) {
    gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
}
"""


FRAG_SHADER = """
#version 120

// Constants
// ------------------------------------
uniform vec4 u_color;


// Main
// ------------------------------------
void main()
{
    gl_FragColor = u_color;
}
"""
