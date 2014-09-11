===============
Design overview
===============


.. digraph:: overview

   size="6,6";
   splines=ortho;
   compound=true;
   node[shape=record, style=filled, fillcolor=gray95]
   edge[dir=back, arrowtail=odiamond, arrowhead=empty]

   graph_node[label = "{Graph | canvas \lartists \l | add_plot(plot) \l}"]
   graph_artist1[label = "{Graph artist 1 | style \l | draw(context, data) \l }"]
   canvas[label = "{Canvas | plots \l | add_plot(plot) \l}"]
   plot1[label = "{Plot 1 | data \ldata_extents \lartists \l\
                   | _render(context) \l}"]
   artist1[label = "{Artist 1 | style \l | draw(context, screen_data) \l }"]

   {rank=same; graph_node; graph_artist1;}
   {rank=same; plot1; artist1;}

   graph_node -> graph_artist1;
   graph_artist1 -> canvas;
   graph_node -> canvas;
   {rank=same; canvas -> plot1};
   plot1 -> artist1;


`Graph`
   The container for a plotting canvas and the decorations around a typical
   plot---e.g. x/y axes, the title, grid lines. This container knows nothing
   about the data.
`Canvas`
   The container where the plotting actually happens. A canvas may contain
   multiple plots---e.g. a line plot and a marker plot. This container observes
   plots to keep track of their data bounds and knows how switch between screen
   and data space.
`*Plot`
   Wrapper objects for data and artists. This object needs to report its data
   extents to the canvas.
`*Artist`
   Flyweight objects that invoke the drawing primitives (e.g. `begin_path()`,
   `stroke_path()`) on the graphics `context`. A given artist expects specific
   keys in the `data` dictionary passed on calls to `draw`. Note that artists
   don't know how to convert between screen and data space, so the plot must
   pass data in screen space.
`data`
   A dictionary of the data to plot. The keys of this dictionary depend on the
   artist. A `LineArtist` might only expect `'x'` and `'y'` to be in the
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
         plots:
            - class: 'line'
              artists:
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