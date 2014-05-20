from deli.core.component import Component
from deli.core.component_editor import ComponentEditor
from deli.core.constraints_container import ConstraintsContainer
from deli.layout.api import align, hbox, vbox
from traits.api import HasTraits, Bool, Instance, Str
from traitsui.api import Item, View, HGroup, VGroup, CodeEditor


class Demo(HasTraits):
    canvas = Instance(ConstraintsContainer)
    child_canvas = Instance(ConstraintsContainer)

    constraints_def = Str
    child_constraints_def = Str
    share_layout = Bool(False)

    traits_view = View(
        HGroup(
            VGroup(
                Item('constraints_def',
                     editor=CodeEditor(),
                     height=100,
                     show_label=False,
                ),
                Item('share_layout'),
                Item('child_constraints_def',
                     editor=CodeEditor(),
                     height=100,
                     show_label=False,
                ),
            ),
            Item('canvas',
                 editor=ComponentEditor(),
                 show_label=False,
            ),
        ),
        resizable=True,
        title="Constraints Demo",
        width=1000,
        height=500,
    )

    def _canvas_default(self):
        parent = ConstraintsContainer(bounds=(500,500), padding=20)

        one = Component(id="r", bgcolor=0xFF0000)
        two = Component(id="g", bgcolor=0x00FF00)
        three = Component(id="b", bgcolor=0x0000FF)

        parent.add(one, two, three, self.child_canvas)
        return parent

    def _child_canvas_default(self):
        parent = ConstraintsContainer(id="child", share_layout=self.share_layout)

        one = Component(id="c", bgcolor=0x00FFFF)
        two = Component(id="m", bgcolor=0xFF00FF)
        three = Component(id="y", bgcolor=0xFFFF00)
        four = Component(id="k", bgcolor=0x000000)

        parent.add(one, two, three, four)
        return parent

    def _constraints_def_changed(self):
        if self.canvas is None:
            return

        canvas = self.canvas
        child = canvas._components[3]

        namespace = {
            'align': align,
            'hbox': hbox,
            'canvas': self.canvas,
            'r': canvas.components[0],
            'g': canvas.components[1],
            'b': canvas.components[2],
            'child': child,
        }

        try:
            new_cns = eval(self.constraints_def, namespace)
        except Exception:
            return

        canvas.layout_constraints = new_cns
        canvas.request_redraw()

    def _child_constraints_def_changed(self):
        if self.child_canvas is None:
            return

        namespace = {
            'align': align,
            'vbox': vbox,
            'canvas': self.canvas,
            'c': self.child_canvas._components[0],
            'm': self.child_canvas._components[1],
            'y': self.child_canvas._components[2],
            'k': self.child_canvas._components[3],
        }

        try:
            new_cns = eval(self.child_constraints_def, namespace)
        except Exception:
            return

        canvas = self.child_canvas
        canvas.layout_constraints = new_cns
        canvas.request_redraw()

    def _share_layout_changed(self):
        self.child_canvas.share_layout = self.share_layout
        self.canvas.relayout()
        self.canvas.request_redraw()

    def _constraints_def_default(self):
        return """[
    hbox(r, g, b, child),
    align('layout_height', r,g,b,child),
    align('layout_width', r,g,b,child),
]"""

    def _child_constraints_def_default(self):
        return """[
    vbox(c,m,y,k),
    align('layout_height', c,m,y,k),
    align('layout_width', c,m,y,k),
]"""


if __name__ == "__main__":
    demo = Demo()
    demo._child_constraints_def_changed()
    demo._constraints_def_changed()
    demo.configure_traits()
