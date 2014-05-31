from .constraints_container import ConstraintsContainer
from deli.layout.api import align, vbox


class Figure(ConstraintsContainer):

    def _layout_constraints_default(self):
        constraints = [
            vbox(*self.components),
            align('layout_height', *self.components)
        ]
        return constraints
