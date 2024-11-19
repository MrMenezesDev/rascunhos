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


def draw_line_between_points(p1, p2, coordinate_scale):
    x1, y1, z1 = [map_value(p1[i], 0, coordinate_scale, -coordinate_scale / 2, coordinate_scale / 2) for i in range(3)]
    x2, y2, z2 = [map_value(p2[i], 0, coordinate_scale, -coordinate_scale / 2, coordinate_scale / 2) for i in range(3)]
    py5.line(x1, y1, z1, x2, y2, z2)

def draw_sphere_at_point(point, color, coordinate_scale, size=5):
    x, y, z = [map_value(point[i], 0, coordinate_scale, -coordinate_scale / 2, coordinate_scale / 2) for i in range(3)]
    py5.push_matrix()
    py5.translate(x, y, z)
    py5.no_fill()
    py5.stroke(*color)
    py5.sphere(size)
    py5.pop_matrix()

def map_value(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))
