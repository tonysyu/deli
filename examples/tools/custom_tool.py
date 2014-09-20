from numpy import linspace

from traits.api import Instance

from deli.demo_utils.traitsui import TraitsWindow
from deli.graph import Graph
from deli.artist.line_artist import LineArtist
from deli.tools.base_tool import BaseTool, BaseToolState
from deli.tools.key_spec import KeySpec, shift_key


class PrintTool(BaseTool):
    """ Tool that prints current mouse position if the shift-key is pressed.

    This tool delegates the actual action to PrintOnMove.
    """

    print_key = shift_key

    def _state_handlers_default(self):
        return {'print': PrintOnMove(self, enabling_key=self.print_key)}

    def on_key_press(self, event):
        if self.print_key.match(event):
            self.state_change(event, new_state='print')


class PrintOnMove(BaseToolState):
    """ Tool state that prints the current position when the mouse is moved.

    Note that this class returns control to the parent tool when the enabling
    key is released.
    """

    enabling_key = Instance(KeySpec)

    def on_mouse_move(self, event):
        print "Mouse at ({}, {})".format(event.x, event.y)

    def on_key_release(self, event):
        if self.enabling_key.match(event):
            self.exit_state(event)


class Demo(TraitsWindow):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Hold shift-key to print coordinates"

        x = y = linspace(0, 1)
        artist = LineArtist(x_data=x, y_data=y)
        graph.add_artist(artist)

        PrintTool.attach_to(graph.canvas)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
