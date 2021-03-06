import numpy as np
from mock import MagicMock

from deli.stylus.line_stylus import LineStylus


POINTS = np.arange(10).reshape(5, 2)


def test_draw():
    stylus = LineStylus()
    context = MagicMock()
    stylus.draw(context, POINTS)

    context.begin_path.assert_called_with()
    context.lines.assert_called_with(POINTS)
    context.stroke_path.assert_called_with()


def test_style_set_during_draw():
    alpha = 0.2
    width = 10
    style = {
        'set_alpha': alpha,
        'set_line_width': width
    }

    stylus = LineStylus(alpha=alpha, width=width)
    context = MagicMock()
    stylus.draw(context, POINTS)

    for method_name, value in style.items():
        method = getattr(context, method_name)
        method.assert_called_with(value)
