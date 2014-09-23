from deli.testing.line_demo import LineDemo


def test_draw():
    demo = LineDemo()
    demo.show()
    demo.context.begin_path.assert_called_with()
    demo.context.stroke_path.assert_called_with()
    demo.context.show_text.assert_called_with(demo.graph.title.text)
