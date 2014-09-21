import numpy as np

from deli.demo_utils.traits_view import TraitsView
from deli.graph import Graph
from deli.artist.line_artist import LineArtist
from deli.tools.data_cursor_tool import DataCursorTool


class Demo(TraitsView):

    def setup_graph(self):
        x = np.linspace(0, 2 * np.pi)
        y1 = np.sin(x)
        y2 = np.cos(x)

        graph = Graph()
        graph.title.text = "Data cursor"

        for y, color in zip((y1, y2), ('black', 'red')):
            artist = LineArtist(x_data=x, y_data=y, color=color)
            graph.add_artist(artist)
            DataCursorTool.attach_to(artist)

        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
