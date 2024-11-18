import py5


def draw_vertex(vertexs, color):
    py5.no_stroke()
    py5.begin_shape()
    py5.fill(color)
    for x, y in vertexs:
        py5.vertex(x, y)
    py5.end_shape(py5.CLOSE),


def draw_map(vertexs, color):
    py5.begin_shape()
    py5.stroke(0)
    py5.stroke_weight(1)
    py5.fill(color)
    for vx, vy in vertexs:
        py5.vertex(vx, vy)
    py5.end_shape(py5.CLOSE)


