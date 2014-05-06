"""
Artist classes for rendering data to screen.

Artist classes are Flyweight classes [GoF]_ that know how to draw items of
interest (e.g., text, lines) and saves the style information about how to draw
these items (e.g. font, color). They **do not**, however, store the data
required to draw individual items (e.g., the text itself, the actual points on
the line).


.. [GoF] Design Patterns: Elements of Reusable Object Oriented Software,
         Gamma et al., Addison-Wesley, 1996.
"""
