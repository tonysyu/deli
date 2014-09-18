===============
Design overview
===============


Core objects
============

.. digraph:: overview

   size="6,6";
   splines=ortho;
   compound=true;
   node[shape=record, style=filled, fillcolor=gray95]
   edge[dir=back, arrowtail=odiamond, arrowhead=empty]

   graph_node[label = "{Graph | canvas \lstyluses \l | add_artist(artist) \l}"]
   graph_stylus1[label = "{Graph stylus 1 | style \l | draw(context, data) \l }"]
   canvas[label = "{Canvas | artists \l | add_artist(artist) \l}"]
   artist1[label = "{Artist 1 | data \ldata_extents \lstyluses \l\
                   | _render(context) \l}"]
   stylus1[label = "{Stylus 1 | style \l | draw(context, screen_data) \l }"]

   {rank=same; graph_node; graph_stylus1;}
   {rank=same; artist1; stylus1;}

   graph_node -> graph_stylus1;
   graph_stylus1 -> canvas;
   graph_node -> canvas;
   {rank=same; canvas -> artist1};
   artist1 -> stylus1;


`Graph`
   The container for a plotting canvas and the decorations around a typical
   plot---e.g. x/y axes, the title, grid lines. This container knows nothing
   about the data.
`Canvas`
   The container where the artist draws plots. A canvas may contain multiple
   artists---e.g. a line artist and a marker artist. This container observes
   artists to keep track of their data bounds and knows how to switch between
   screen and data space.
`*Artist`
   Wrapper objects for data and styluses. This object needs to report its data
   extents to the canvas.
`*Stylus`
   Flyweight objects that invoke the drawing primitives (e.g. `begin_path()`,
   `stroke_path()`) on the graphics `context`. A given stylus expects specific
   keys in the `data` dictionary passed on calls to `draw`. Note that styluses
   don't know how to convert between screen and data space, so the artist must
   pass data in screen space.
`data`
   A dictionary of the data to plot. The keys of this dictionary depend on the
   stylus. A `LineStylus` might only expect `'x'` and `'y'` to be in the
   dictionary.
`style`
   A dictionary containing style information (color, line-width, etc)

::

   graph:

      title:
         text: 'A simple plot'

      x-axis:
         ticks: [1, 2, 3]
      y-axis:
         ticks: [10, 20, 30]

      canvas:
         bounds: [0, 0, 400, 600]
         artists:
            - class: 'line'
              styluses:
                 - class:'line'
                   style:
                      color: 'black'
                      linewidth: 1
                 - class:'marker'
                   style:
                      color: 'black'
                      linewidth: 1
              data:
                 x: [1, 2, 3]
                 y: [10, 20, 30]


Rendering cascade
=================

Rendering to the screen has a few moving parts. The lowest level that we'll
discuss here is the `graphics context`. This is that part of the rendering
code that provides an interface between the generic parts of the deli codebase
and the underlying GUI toolkit. (Actually, it doesn't have to be a GUI toolkit
if, for example, you only care about drawing to a document.) The graphics
context abstracts out toolkit-specific details into simple line-drawing,
text-drawing, etc. commands. If you've worked with HTML5 canvas, then you
should be pretty familiar with graphics contexts.

The top-level window (also GUI-toolkit specific) is in charge of creating the
graphics context and passing it down to all the graphics components. Actually,
all it does is pass it down to the top-most graphics component---typically,
`Graph`---and that graphics component passes the graphics context down to its
children. So that top-level window would just call:


.. code-block:: python

   graph.render(context)

And `graph` will make sure all its child components have an opportunity to draw
onto that graphics context. The `render` method for `graph` might look a little
something like:

.. code-block:: python

   def render(self, context):
       self.draw(context)
       for child in self.children:
           child.render(context)

Note that this calls `render` on child components and it calls `draw` on
itself. This `draw` method gives an opportunity for the component to actually
draw something to the context (rather just passing along the context to its
children). Think of `draw` as `draw_self` and `render` as
`draw_self_and_children`.
