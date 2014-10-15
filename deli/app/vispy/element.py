from abc import ABCMeta, abstractmethod
from contextlib import contextmanager

from vispy import gloo
from vispy.gloo import gl


class GLElement(object):

    __metaclass__ = ABCMeta

    def __init__(self, vert_shader, frag_shader):
        self._program = gloo.Program(vert_shader, frag_shader)

    def __setitem__(self, key, value):
        self._program[key] = value

    def update(self, state):
        self._rect_clip = state.rect_clip

    @abstractmethod
    def draw(self):
        """ Draw this graphics element.

        Typically, this will draw under `self._draw_context`.
        """

    @contextmanager
    def _draw_context(self):
        if self._rect_clip is None:
            yield
        else:
            gl.glEnable(gl.GL_SCISSOR_TEST);
            gloo.set_scissor(*self._rect_clip)
            yield
            gl.glDisable(gl.GL_SCISSOR_TEST);


def create_program(data, vert_shader, frag_shader):
    """Return gloo.Program for drawing data with the given shaders. """
    program = gloo.Program(vert_shader, frag_shader)
    vertex_buffer = gloo.VertexBuffer(data)
    program.bind(vertex_buffer)
    return program


def set_program_data(program, data):
    vertex_buffer = gloo.VertexBuffer(data)
    program.bind(vertex_buffer)
