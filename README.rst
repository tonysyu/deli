====
Deli
====

Yet another plotting library for Python.

Currently, this library isn't meant for public consumption. I'm just using this
as an outlet for exploring some design patterns and playing around with fixes
for things that bother me about existing plotting tools.

See the ``examples`` directory to get a general feel for the API. These
examples are also very minimal at the moment.


Roadmap
=======

* Integrate constraints-based layout
* Rewrite layer-drawing dispatch
* Generalize rendering backend (for Vispy, javascript, etc. interfaces)
* Simplify ``Components`` and ``Container`` objects
* Add typical plotting functionality (axis labels, bar charts, legends, etc.)
* Add scripting interfaces (a la, ``matplotlib.pyplot``, ``ggplot``, etc.)


Requirements
============

* numpy
* traits

The following requirements will, hopefully, be removed in the future:
* pyface
* enable
* kiva
* matplotlib

The following are optional requirements:
* enaml (optional)
* traitsui (optional)
* vispy (optional)


Licence
=======

New BSD (a.k.a. Modified BSD). See ``LICENSE`` in this directory for details.


Origin story
============

I started to learn Python while looking for a good plotting package for one of
my first research papers. My research advisor suggested GnuPlot, but after
looking at it for an afternoon, I was convinced that it was not what I wanted
to spend my time using. Eventually, I settled on PyX_, which produced
beautiful figures, especially compared to what Matlab (which is what I used for
my data analysis) could produce at the time (circa 2006). After that paper,
I moved on to using and contributing to matplotlib_ (one of the
more popular plotting libraries in Python). I also played around with chaco_
during my graduate studies and use it extensively now, since I started work at
`Enthought Inc.`_.

That's all to say: I've used a few plotting libraries in Python, and I know
there are many recent additions to the mix. They all have their strengths (and
their weakness), and they were all created by very smart people. I don't claim
to have a better design than they do (although secretly, I kind of want to
think that). The whole point of this project is for me to play around with a
few ideas that have come up over time.


.. _PyX: http://pyx.sourceforge.net/
.. _matplotlib: http://matplotlib.sourceforge.net/
.. _mpltools: http://tonysyu.github.com/mpltools
.. _chaco: https://chaco.readthedocs.org/en/latest/
.. _Enthought Inc.:  http://enthought.com/
.. [GoF] Design Patterns: Elements of Reusable Object Oriented Software,
         Gamma et al., Addison-Wesley, 1996.
