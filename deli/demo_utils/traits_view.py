from __future__ import absolute_import

from abc import abstractmethod

from traits.api import ABCHasStrictTraits, Bool, Instance, Str, Tuple
from traitsui.api import UItem, View

from ..core.constraints_container import ConstraintsContainer
from ..graph import Graph
from ..layout.api import align, vbox
from ..tools.pan_tool import PanTool
from ..tools.zoom_tool import ZoomTool
from .traitsui_editor import ComponentEditor


WIDTH = 700
HEIGHT = 500


class TraitsView(ABCHasStrictTraits):
    """ A simple TraitsUI window for displaying a Graph """

    title = Str
    size = Tuple((WIDTH, HEIGHT))
    graph = Instance(Graph)

    zoom_and_pan = Bool(True)

    def default_traits_view(self):
        view = View(
            UItem('graph', editor=ComponentEditor(size=self.size)),
            resizable=True, title=self.title,
        )
        return view

    @abstractmethod
    def setup_graph(self):
        """ Create `Graph` to display in the window. """

    def _graph_default(self):
        graph = self.setup_graph()

        if self.zoom_and_pan:
            ZoomTool.attach_to(graph)
            PanTool.attach_to(graph.canvas)
        return graph

    def show(self):
        self.configure_traits()


class FigureView(ABCHasStrictTraits):
    """ A TraitsUI window displaying multiple Graphs objects. """

    title = Str
    size = Tuple((WIDTH, HEIGHT))
    figure = Instance(ConstraintsContainer)
    zoom_and_pan = Bool(True)

    def default_traits_view(self):
        view = View(
            UItem('figure', editor=ComponentEditor(size=self.size)),
            resizable=True, title=self.title,
        )
        return view

    @abstractmethod
    def create_graphs(self):
        """ Create and return `Graph` objects for plotting. """

    def show(self):
        graphs = self.create_graphs()

        if self.zoom_and_pan:
            for g in graphs:
                ZoomTool.attach_to(g)
                PanTool.attach_to(g.canvas)

        self.figure = ConstraintsContainer(size=(500, 500))
        self.figure.add(*graphs)
        self.figure.layout_constraints = [
            vbox(*graphs),
            align('layout_height', *graphs),
        ]

        self.configure_traits()
