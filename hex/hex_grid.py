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
    state_colors: List[List[str]] = field(default_factory=list)
    inner_scale: float = 0.29  # fator do hex pequeno central ("cubo") relativo a self.size
    inner_colors: List[str] | None = None  # paleta específica do hex interno (3 cores)

    def __post_init__(self):
        # Dimensões base do hex
        self.hex_height = math.sin(math.pi * 2 / 6) * self.size * 2
        self.hex_width = self.size * 1.5
        self.offset = self.size
        # Estados
        self.state = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.state_colors = [["" for _ in range(self.cols)] for _ in range(self.rows)]
        if self.inner_colors is None:
            # Usa cópia para permitir alterar sem afetar self.colors
            self.inner_colors = list(self.colors)

    def set_state(self, evolution_history, step):
        self.state = evolution_history[step]

    def calculate_center(self, row: int, col: int) -> Tuple[float, float]:
        """
        Calcula o centro do hexágono baseado na linha e coluna.
        """
        offset_y = self.hex_height / 2 if col % 2 == 1 else 0
        center_x = col * self.hex_width + self.offset
        center_y = row * self.hex_height + offset_y + self.offset
        return center_x, center_y

    def get_tile_color(self, x: int, y: int) -> str:
        row, col = self.get_cell_at(x, y)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.state_colors[row][col]
        return None
    
    def change_tile_color(self, x: int, y: int, new_color: str):
        row, col = self.get_cell_at(x, y)   
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.state[row][
                col
            ] = 1  # Adicione esta linha para garantir que o estado seja 1
            self.state_colors[row][col] = new_color
            print(
                f"Drawing hexagon at ({x}, {y}) in row {row} and col {col} with color  {new_color}"
            )  # Adicione esta linha
            center_x, center_y = self.calculate_center(x, y)
            self.draw_hexagon(center_x, center_y, self.size, color=new_color)
       

    def get_cell_at(self, x: float, y: float) -> Tuple[int, int]:
        """
        Recebe uma coordenada (x, y) e retorna a célula (row, col) que está sobre essa coordenada.
        """
        col = int(x // self.hex_width)
        row = int((y - (col % 2) * self.hex_height / 2) // self.hex_height)

        # Verifica se a coordenada está dentro dos limites da grade
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return row, col
        else:
            return -1, -1

    def draw_base(self):
        """Desenha apenas o hex externo para toda a grade."""
        for y in range(self.rows):
            for x in range(self.cols):
                center_x, center_y = self.calculate_center(x, y)
                if self.state[y][x] == 1:
                    color = (
                        self.state_colors[y][x]
                        if self.state_colors[y][x]
                        else self.colors[0]
                    )
                    self.draw_hexagon(center_x, center_y, self.size, color=color)
                else:
                    self.draw_hexagon(center_x, center_y, self.size)

    def draw_inner(self):
        """Desenha apenas o hex interno (cubo estilizado) por célula vazia."""
        for y in range(self.rows):
            for x in range(self.cols):
                if self.state[y][x] == 1:
                    continue
                center_x, center_y = self.calculate_center(x, y)
                inner = max(0.02, min(0.95, self.inner_scale))
                palette = self.inner_colors if self.inner_colors else self.colors
                self.draw_hexagon(
                    center_x,
                    center_y,
                    self.size * inner,
                    math.pi * 2 / 12,
                    palette,
                )

    def draw(self):
        """Mantém compatibilidade chamando base + inner."""
        self.draw_base()
        self.draw_inner()

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

    def draw_parallel_shapes(self, x, y, x1, y1, colors, angle=30, factor=-1, start_offset: float = 0.0):
        # Vetor principal
        dx = x1 - x
        dy = y1 - y
        length = (dx * dx + dy * dy) ** 0.5
        if length <= 1e-9:
            return
        # Ajusta offset se solicitado (não deixa exceder 80% do comprimento para manter forma)
        if start_offset > 0:
            if start_offset >= length * 0.95:  # evita degenerar
                start_offset = length * 0.95
            ux, uy = dx / length, dy / length
            x += ux * start_offset
            y += uy * start_offset
            dx = x1 - x
            dy = y1 - y
            length = (dx * dx + dy * dy) ** 0.5
            if length <= 1e-9:
                return
        # Perpendicular para espessura visual
        perp_x = -dy / length * self.size / 4
        perp_y = dx / length * self.size / 4
        # Pontos deslocados
        x2, y2 = x + perp_x, y + perp_y
        x3, y3 = x1 + perp_x, y1 + perp_y
        x4, y4 = x - perp_x, y - perp_y
        x5, y5 = x1 - perp_x, y1 - perp_y
        # Interseções rotacionadas para formar polígonos
        xi, yi = line_intersection(
            x, y, *get_rotation_in_line(x, y, x2, y2, angle * factor), x3, y3, x2, y2
        )
        vertex_initial = [(x, y), (x1, y1), (x3, y3), (xi, yi)]
        self.draw_vertex(vertex_initial, colors[0])
        xin, yin = line_intersection(
            x, y, *get_rotation_in_line(x, y, x4, y4, -angle * factor), x5, y5, x4, y4
        )
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
            # Restaura lógica original: iterar base_i em [-2,0,2] => (4,0,2) e usar colors[i]
            # Para lista de 3, colors[-2] == colors[1]. Portanto ordem aplicada: colors[1], colors[0], colors[2]
            for i in [-2, 0, 2]:
                base_i = i % 6
                prev_i = (base_i - 1) % 6
                next_i = (base_i + 1) % 6
                color_hex = colors[i]
                self.draw_vertex([
                    (x, y),
                    (vertices[prev_i][0], vertices[prev_i][1]),
                    (vertices[base_i][0], vertices[base_i][1]),
                    (vertices[next_i][0], vertices[next_i][1]),
                ], color_hex)
        else:
            self.draw_map(vertices, color)

        return vertices
