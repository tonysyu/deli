from traits.api import HasStrictTraits, Instance
from traitsui.api import UItem, View

from deli.core.constraints_container import ConstraintsContainer
from deli.core.component import Component
from deli.core.figure import Figure
from deli.demo_utils.traitsui_editor import ComponentEditor
from deli.style.colors import default_cycle


class Demo(HasStrictTraits):

    figure = Instance(Figure)

    traits_view = View(
        UItem('figure', editor=ComponentEditor()),
        resizable=True,
    )

    def _figure_default(self):
        figure = Figure(bgcolor=default_cycle.next())
        a = ConstraintsContainer(bgcolor=default_cycle.next())
        # Try a component just to make sure things work as expected
        b = Component(bgcolor=default_cycle.next())
        figure.add(a, b)
        return figure

    def show(self):
        self.configure_traits()


if __name__ == "__main__":
    demo = Demo()
    demo.show()
