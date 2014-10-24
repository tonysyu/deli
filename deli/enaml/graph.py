from atom.api import List, Str, Typed, set_default
from enaml.core.declarative import d_
from enaml.widgets.api import RawWidget

from ..graph import Graph as GraphComponent
from ..app.window import Window
from ..core.component import Component
from .base_artist import BaseArtist


class Graph(RawWidget):
    """ A widget that displays a graph containing artists. """

    #: The artists added to the graph.
    artists = d_(List(Typed(BaseArtist)))

    title = d_(Str())

    #: The deli component to be displayed
    _component = d_(Typed(Component))

    #: Internal storage for the enable window
    _window = Typed(Window)

    # Initialize window to specified size but allow resizing.
    hug_width = set_default('weak')
    hug_height = set_default('weak')
    resist_width = set_default('weak')
    resist_height = set_default('weak')

    def create_widget(self, parent):
        self._component = GraphComponent()
        self._component.title.text = self.title

        for artist in self._iter_artists():
            self._component.add_artist(artist)

        self._window = Window(parent, component=self._component,
                              size=(700, 500),
                              bgcolor=self._component.bgcolor)
        return self._window.control

    def _iter_artists(self):
        """ Yield deli artist instances. """
        for child in self.children:
            if isinstance(child, BaseArtist) and child.deli_artist is not None:
                yield child.deli_artist
