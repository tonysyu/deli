from numpy import linspace
from scipy.special import jn

from deli.demo_utils.traits_view import TraitsView
from deli.graph import Graph
from deli.artist.line_artist import LineArtist
from deli.style.colors import default_cycle


class Demo(TraitsView):

    def setup_graph(self):
        graph = Graph()
        graph.title.text = "Line Artist"

        x = linspace(-2.0, 10.0, 100)
        for i in range(5):
            y = jn(i, x)
            artist = LineArtist(x_data=x, y_data=y, color=default_cycle.next())
            graph.add_artist(artist)
        return graph


if __name__ == '__main__':
    demo = Demo()
    demo.show()
