=========================================
Deli: Another plotting library for Python
=========================================


Currently, this library isn't meant for public consumption. I'm using this as
a venue for exploring some design patterns and playing around with fixes for
things that bother me about existing plotting tools.


Origin story
------------

I started to learn Python while looking for a good plotting package for one of
my first research papers. My research advisor suggested GnuPlot, but after
looking at it for an afternoon, I was convinced that it was not what I wanted
to spend my time using. Eventually, I settled on PyX [pyx]_, which produced
beautiful figures, especially compared to what Matlab (which is what I used for
my data analysis) could produce at the time (circa 2006). After that paper,
I moved on to using and contributing to Matplotlib [matplotlib]_ (one of the
more popular plotting libraries in Python). I also played around with `Chaco`
during my graduate studies and use it extensively now, since I started work at
Enthought Inc. [enthought]_,

That's all to say: I've used a few plotting libraries in Python, and I know
there are many recent additions to the mix. They all have their strengths (and
their weakness), and they were all created by very smart people. I don't claim
to have a better design than they do (although secretly, I kind of want to
think that). The whole point of this project is for me to play around with a
few ideas that have come up over time.

This project got it's start as I was finishing the Design Patterns book [GoF]_
for the first time. (I'm not a software developer by training, so I read it
rather late in life.)


Why "Deli"
----------

I actually wanted to name this package "SpyGlass", which is an area of Austin,
TX and a really great name for a data-visualization package. Alas, that name
is already taken in PyPi. For some reason, I was stuck with naming it something
Austin-related, and decided to name it after a popular taco place here,
TacoDeli. It's a bit appropriate,... I guess: Plotting is nothing if not
a highly customized way of ... ____


.. _pyx: http://pyx.sourceforge.net/
.. _matplotlib: http://matplotlib.sourceforge.net/
.. _mpltools: http://tonysyu.github.com/mpltools
.. _enthought:  http://enthought.com/
.. [GoF] Design Patterns: Elements of Reusable Object Oriented Software,
         Gamma et al., Addison-Wesley, 1996.
