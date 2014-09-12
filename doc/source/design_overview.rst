===============
Design overview
===============


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
