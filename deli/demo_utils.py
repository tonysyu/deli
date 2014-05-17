from abc import abstractmethod

from traits.api import ABCHasStrictTraits, Bool, Instance, Str, Tuple
from traitsui.api import UItem, View

from deli.core.component_editor import ComponentEditor
from deli.plot_canvas import PlotCanvas
from deli.tools.pan_tool import PanTool
from deli.tools.zoom_tool import ZoomTool


class Window(ABCHasStrictTraits):
    """ A simple TraitsUI window for displaying a PlotCanvas """

    title = Str
    size = Tuple((700, 500))
    canvas = Instance(PlotCanvas)

    zoom_and_pan = Bool(True)

    def default_traits_view(self):
        view = View(
            UItem('canvas', editor=ComponentEditor(size=self.size)),
            resizable=True, title=self.title
        )
        return view

    @abstractmethod
    def setup_canvas(self):
        """ Create `PlotCanvas` to display in the window. """

    def _canvas_default(self):
        canvas = self.setup_canvas()

        if self.zoom_and_pan:
            ZoomTool.attach_to(canvas)
            PanTool.attach_to(canvas)
        return canvas
