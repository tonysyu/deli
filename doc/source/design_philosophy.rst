=================
Design philosophy
=================


This project got its start as I was finishing the Design Patterns book [GoF]_
for the first time. As a result, there are probably more than a few
mis-applications of design patterns in this code. In addition, I've worked a
bit with both the matplotlib_ and chaco_ code bases. Both have their merits,
but as anyone who's used any library ever can relate to: There are decisions
which that I wish 

The core design philosophy is that most of the functionality should be provided
by small objects, methods, and utility functions. Yes, that's a good guiding
principle in general, but more-so in plotting, where customization and
composition are so critical.

Part of the design was a reaction to Chaco and Matplotlib.

* Use ``x``, ``y`` (and ``z``) to represent ``index`` and ``value`` from Chaco

  - ``index`` is too easily confused with array indices.
  - ``value`` is the least informative name ever.
  - Changing the behavior of ``index`` and ``value`` (e.g. for image plots)
    just to remain consistent with their names is a bad idea.

* Use Matplotlib's bounding box and transform implementations instead of
  Chaco's mappers.

* Plot functions should be decentralized; I'm looking at you ``Axes``
  (Matplotlib) and ``Plot`` (Chaco).

  - God-classes are a bad idea.

And a few random ideas.

* Use Stylus primitives for drawing.

  - Styluses are Flyweights (see [GoF]_) with interfaces for different
    parameters inputs and little, if any, knowledge of the data. Instead data
    is passed in at draw time with only 
  - An stylus defines its own graphics context which updates its own settings
    (color, alpha, anti-aliasing, etc.) but you can pass in any
    instance-specific parameters you like to override the stylus default

* State should be a simple dict


Naming conventions
==================

Naming is important, and so is consistency.

Basic structure
---------------

An artist draws on a canvas with styluses.

stylus:
   Rendering objects that know how to draw primitive objects (e.g. lines,
   bars, etc.). Stylus instances have all the style information needed these
   primitives, but doesn't hold any data. These should be passed at draw time.
artist:
   A simple object that combines styluses and data.
canvas:
   The area where a plot is drawn. A plot-canvas may be composed of multiple
   "plots". For example, point data maybe drawn as a line-plot and
   a marker-plot on the same plot-canvas.
graph:
   This is what people normally refer to as a "plot". The graph includes the
   plot-canvas, plus axes, titles, etc. This is referred to as an `axes` in
   matplotlib and a (capital-"P") `Plot` in chaco.
figure:
   A figure is a composition of graphs.


Coordinates
-----------

* data values are simply ``x``, ``y``, ``z``
   - when arrays are 2D: ``xx``, ``yy``, ``zz``
* Use ``i_`` prefix is always an index into an array
* array indices use row/col specifier
* Use ``axial`` and ``ortho`` to specify general coordinate directions.
* screen values use ``px`` specifier (``x_px_size``)
* Relative positions named ``offsets`` for single coordinate, ``xy_offsets``
  for x-y coordinate offset.


Bounds, ranges, and limits
--------------------------

* Use ``_limits`` and ``_min``/``_max`` suffixes for absolute bounds
* Use ``_range`` and ``_lo``/``_hi`` suffixes for "current" (displayed or
  operational) bounds
* ``span``: length of bounds.
* Everything should have a bbox parameter (this replaces components' (x, y,
  width,height)


.. [GoF] Design Patterns: Elements of Reusable Object Oriented Software,
         Gamma et al., Addison-Wesley, 1996.

.. _matplotlib: http://matplotlib.sourceforge.net/

.. _chaco: http://docs.enthought.com/chaco/
