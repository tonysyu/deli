from atom.api import Typed, observe, set_default
from enaml.widgets.api import RawWidget
from enaml.core.declarative import d_

from ..core.window import Window
from ..core.component import Component


class EnamlWidget(RawWidget):
    """ A widget that displays deli component

    :Attributes:
        **component** = *d_(Typed(Component))*
            The enable component to be displayed

    """
    #: The deli component to be displayed
    component = d_(Typed(Component))

    #: Internal storage for the enable window
    _window = Typed(Window)

    #: Deli canvases expand freely in width and height by default
    hug_width = set_default('ignore')
    hug_height = set_default('ignore')

    def create_widget(self, parent):
        if self.component is not None:
            self._window = Window(parent, component=self.component,
                                  bgcolor=self.component.bgcolor)
            widget = self._window.control
        else:
            self._window = None
            widget = None

        return widget

    @observe('component')
    def component_changed(self, new):
        if self._window is not None:
            self._window.component = new['value']
