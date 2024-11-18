import math
from dataclasses import dataclass, field
from typing import List, Callable, Tuple
from utils.math_utils import get_rotation_in_line, line_intersection

@dataclass
class HexGrid:
    cols: int
    rows: int
    size: float
    draw_vertex: Callable
    draw_map: Callable
    colors: List[str] = field(default_factory=lambda: ["#666666", "#999999", "#333333"])
    cells: List = field(default_factory=list)
    hex_height: float = field(init=False)
    hex_width: float = field(init=False)
    offset: float = field(init=False)
    state: List[List[int]] = field(default_factory=list)

    def __post_init__(self):
        self.hex_height = math.sin(math.pi * 2 / 6) * self.size * 2  # Altura do hexágono
        self.hex_width = self.size * 1.5  # Largura do hexágono
        self.offset = self.size
    
        self.state = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
    
    def set_state(self, evolution_history, step):
        """
        Define o estado das células com base no evolution_history e no passo atual.
        """
        self.state = evolution_history[step]


    def calculate_center(self, col: int, row: int) -> Tuple[float, float]:
        """
        Calcula o centro do hexágono baseado na coluna e linha.
        """
        offset_y = self.hex_height / 2 if col % 2 == 1 else 0
        center_x = col * self.hex_width + self.offset
        center_y = row * self.hex_height + offset_y + self.offset
        return center_x, center_y

    def draw(self):
        for y in range(self.rows):
            for x in range(self.cols):
                center_x, center_y = self.calculate_center(x, y)
                if self.state[y][x] == 1:
                    self.draw_hexagon(center_x, center_y, self.size, color=1)
                else:
                    self.draw_hexagon(center_x, center_y, self.size)
                    # Desenhar um hexágono menor no centro
                    self.draw_hexagon(center_x, center_y, self.size * 0.29, math.pi * 2 / 12, self.colors)

    def draw_cell(self, cell):
        """
        Este método desenha um caminho do centro do hexágono até a borda do hexágono.
        O caminho é desenhado apenas se a célula estiver colapsada.
        Pode ser desenhadas 0 a 6 linhas, sendo elas 0 o topo.
        Cada edge representa uma direção e o valor 1 indica que a borda está conectada.
        """
        if not cell.collapsed:
            return

        center_x, center_y = self.calculate_center(cell.col, cell.row)
        size = self.size

        for i in [3, 5, 1, 2, 4, 0]:
            edge = cell.tile.edges[i]
            index = [4, -1, 0, 1, 2, 3][i]
            if edge == 1:
                
                # Calcular os ângulos dos dois vértices que formam a borda
                angle1 = math.pi * 2 / 6 * index
                angle2 = math.pi * 2 / 6 * ((index + 1) % 6)

                # Calcular a posição dos dois vértices
                vertex1_x = center_x + math.cos(angle1) * size
                vertex1_y = center_y + math.sin(angle1) * size
                vertex2_x = center_x + math.cos(angle2) * size
                vertex2_y = center_y + math.sin(angle2) * size

                # Calcular a posição do ponto médio da borda
                edge_x = (vertex1_x + vertex2_x) / 2
                edge_y = (vertex1_y + vertex2_y) / 2

                # Definir as cores das linhas
                color = [[0, 5, 8, 9], [3, 4, 6, 7], [1, 2, 10, 11]]
                c1 = (
                    self.colors[2]
                    if (i + 6) in color[0]
                    else self.colors[0] if (i + 6) in color[1] else self.colors[1]
                )
                c2 = (
                    self.colors[2]
                    if i in color[0]
                    else self.colors[0] if i in color[1] else self.colors[1]
                )

                # Draw parallel lines
                self.draw_parallel_shapes(center_x, center_y, edge_x, edge_y, [c1, c2])

        return (f"{cell.col},{cell.row}", center_x, center_y)

    def draw_parallel_shapes(self, x, y, x1, y1, colors, angle=30, factor=-1):
        # Calcular o vetor perpendicular
        dx = x1 - x
        dy = y1 - y
        length = (dx**2 + dy**2) ** 0.5
        perp_x = -dy / length * self.size / 4
        perp_y = dx / length * self.size / 4

        # Calcular as novas posições para as linhas paralelas
        x2, y2 = x + perp_x, y + perp_y
        x3, y3 = x1 + perp_x, y1 + perp_y
        x4, y4 = x - perp_x, y - perp_y
        x5, y5 = x1 - perp_x, y1 - perp_y

        xi, yi = line_intersection(
            x, y, *get_rotation_in_line(x, y, x2, y2, angle * factor), x3, y3, x2, y2
        )

        # Desenhar a linha principal
        vertex_initial = [(x, y), (x1, y1), (x3, y3), (xi, yi)]

        self.draw_vertex(vertex_initial, colors[0])

        xin, yin = line_intersection(
            x, y, *get_rotation_in_line(x, y, x4, y4, -angle * factor), x5, y5, x4, y4
        )

        # Desenhar a forma paralela
        vertex_parallel = [(x, y), (x1, y1), (x5, y5), (xin, yin)]
        self.draw_vertex(vertex_parallel, colors[1])

    def draw_hexagon(self, x, y, size, rotation=0, colors=None, color=255):
        # Calcular os vértices do hexágono
        vertices = []
        for i in range(6):
            angle = (math.pi * 2 / 6 * i) + rotation
            vx = x + math.cos(angle) * size
            vy = y + math.sin(angle) * size
            vertices.append((vx, vy))

        # Desenhar os losângulos
        if colors and len(colors) >= 3:
            for i in [-2, 0, 2]:
                self.draw_vertex([
                    (x, y),
                    (vertices[i - 1][0], vertices[i - 1][1]),
                    (vertices[i][0], vertices[i][1]),
                    (vertices[i + 1][0], vertices[i + 1][1]),
                ], colors[i])
        else:
            self.draw_map(vertices, color)

        return vertices

