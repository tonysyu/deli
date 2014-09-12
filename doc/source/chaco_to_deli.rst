================================
Transitioning from chaco to deli
================================

Some of these changes are describe more thoroughly in design_philosophy_, but
this gives a quick guide for someone transitioning from Chaco.

* Use ``x``, ``y`` to represent ``index`` and ``value`` from Chaco
* Mappers are completely removed in favor of Matplotlib's bounding-box and
  transforms architecture.
* (Capital-"P") ``Plot`` is renamed ``Canvas``, but it's drastically
  different in the sense that it provides a thin plotting container.
* The name "plot" is restricted to things that are sometimes called "renderers"
  in Chaco ("plot" methods/functions do not exist)
