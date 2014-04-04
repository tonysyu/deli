""" Defines a base class for plot renderers.
"""
from traits.api import Enum

from plot_component import PlotComponent


class AbstractPlotRenderer(PlotComponent):
    """ This is the minimal interface that all plot renderers must support.

    This interface exists mostly to support the development of generic
    interactors and plot tools.
    """

    origin = Enum("bottom left", "top left", "bottom right", "top right")

    bgcolor = "transparent"

    resizable = "hv"
