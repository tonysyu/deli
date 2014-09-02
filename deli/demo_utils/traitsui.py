from __future__ import absolute_import

from abc import abstractmethod

from traits.api import ABCHasStrictTraits, Bool, Instance, Str, Tuple
from traitsui.api import UItem, View

from .traitsui_editor import ComponentEditor
from ..graph import Graph
from ..tools.pan_tool import PanTool
from ..tools.zoom_tool import ZoomTool


WIDTH = 700
HEIGHT = 500


class TraitsWindow(ABCHasStrictTraits):
    """ A simple TraitsUI window for displaying a Graph """

    title = Str
    size = Tuple((WIDTH, HEIGHT))
    graph = Instance(Graph)

    zoom_and_pan = Bool(True)

    def default_traits_view(self):
        view = View(
            UItem('graph', editor=ComponentEditor(size=self.size)),
            resizable=True, title=self.title
        )
        return view

    @abstractmethod
    def setup_graph(self):
        """ Create `Graph` to display in the window. """

    def _graph_default(self):
        graph = self.setup_graph()

        if self.zoom_and_pan:
            ZoomTool.attach_to(graph.canvas)
            PanTool.attach_to(graph.canvas)
        return graph

    def show(self):
        self.configure_traits()
