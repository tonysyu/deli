"""
Renderer classes for ... umm ... rendering data to screen.

Unlike artists, renderers may contain the data that they render. Renderers
are simply specific types of plots: For example, line-plots, marker-plots,
and bar-plots, may all be the same data associated with different renderers.
As a result, renderers may use a few different artists to compose a plot;
for example, a box-and-whisker plot might have separate artists to draw
rectangles, error-bars (whiskers), and points (outliers).

"""
