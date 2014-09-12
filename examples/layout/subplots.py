import numpy as np

from traits.api import HasStrictTraits, Instance
from traitsui.api import Item, View

from deli.demo_utils.traitsui_editor import ComponentEditor
from deli.core.constraints_container import ConstraintsContainer
from deli.layout.api import align, vbox
from deli.graph import Graph
from deli.artist.line_artist import LineArtist
from deli.artist.scatter_artist import ScatterArtist


class Demo(HasStrictTraits):

    figure = Instance(ConstraintsContainer)
    line_graph = Instance(Graph)
    scatter_graph = Instance(Graph)

    traits_view = View(
        Item('figure',
             editor=ComponentEditor(),
             show_label=False,
        ),
        resizable=True,
        title="Subplots using constraints container",
        width=500, height=500,
    )

    def _figure_default(self):
        figure = ConstraintsContainer(size=(500, 500))

        figure.add(self.line_graph, self.scatter_graph)
        figure.layout_constraints = [
            vbox(self.line_graph, self.scatter_graph),
            align('layout_height', self.line_graph, self.scatter_graph),
        ]
        return figure

    def _line_graph_default(self):
        graph = Graph()
        graph.title.text = "Line Artist"

        x = np.linspace(0, 10.0, 100)
        artist = LineArtist(x_data=x, y_data=np.sin(x))
        graph.add_artist(artist)
        return graph

    def _scatter_graph_default(self):
        graph = Graph()
        graph.title.text = "Scatter Artist"

        x = np.linspace(0, 10.0, 100)
        artist = ScatterArtist(x_data=x, y_data=np.sin(x))
        graph.add_artist(artist)
        return graph

    def show(self):
        self.configure_traits()


if __name__ == "__main__":
    demo = Demo()
    demo.show()
