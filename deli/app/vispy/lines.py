import numpy as np


def data(points, line_width=1, color=(0, 0, 0, 1)):
    """ Return data and fragment shader for markers. """
    x, y = np.transpose(points)
    positions = np.transpose([x, y, np.zeros_like(x)])

    n = len(x)

    a_id = np.random.randint(0, 30, n)
    a_id = np.sort(a_id, axis=0).astype(np.float32)
    data = np.zeros(n, dtype=[('a_position', np.float32, 3),
                              ('a_id', np.float32)])
    # data = np.zeros(n, dtype=[('a_position', np.float32, 3),
                              # ('a_fg_color', np.float32, 4),
                              # ('a_bg_color', np.float32, 4),
                              # ('a_size', np.float32, 1),
                              # ('a_linewidth', np.float32, 1)])
    data['a_position'] = positions
    data['a_id'] = a_id
    # data['a_size'] = 1
    # data['a_fg_color'] = color
    # data['a_bg_color'] = color
    # data['a_linewidth'] = line_width

    return data, frag_shader


vert_shader = """
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_antialias;
uniform float u_size;

attribute vec3 a_position;
attribute float a_id;

varying float v_id;

void main (void) {
    v_id = a_id;
    gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
}
"""

frag_shader = """
varying float v_id;

void main()
{
    gl_FragColor = vec4(0,0,0,1);
}
"""
