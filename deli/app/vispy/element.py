from abc import ABCMeta, abstractmethod

from vispy import gloo


class GLElement(object):

    __metaclass__ = ABCMeta

    def __setitem__(self, key, value):
        self._program[key] = value

    @abstractmethod
    def draw(self):
        self._program.draw('line_strip')


def create_program(data, vert_shader, frag_shader):
    """Return gloo.Program for drawing data with the given shaders. """
    program = gloo.Program(vert_shader, frag_shader)
    vertex_buffer = gloo.VertexBuffer(data)
    program.bind(vertex_buffer)
    return program
