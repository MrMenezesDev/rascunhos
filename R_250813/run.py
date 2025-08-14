"""Gerador Interativo de Ladrilhos Hexagonais
================================================
Instruções rápidas:
  Mouse ESQUERDO: alterna a borda mais próxima na célula clicada
  SHIFT + ESQUERDO: liga TODAS as bordas da célula
  CTRL  + ESQUERDO: desliga TODAS as bordas da célula
  Mouse DIREITO: limpa a célula
  Tecla S: exporta padrões únicos em tiles.json
  Tecla R: reseta toda a grade
  Tecla H: mostra / oculta esta ajuda
  Tecla C: copia (imprime) o padrão da célula sob o mouse

O arquivo gerado tiles.json contém uma lista de objetos:
  {"id": n, "edges": [e0,e1,e2,e3,e4,e5]}

Os índices de edges seguem a convenção:
  0 = topo (aresta horizontal superior)
  Prossegue no sentido horário.

Este script reutiliza utilidades de desenho já existentes em HexGrid para manter
o mesmo estilo visual (linhas paralelas sombreando as conexões) usado no WFC.
"""

from __future__ import annotations
import math
import json
from pathlib import Path
import random
import py5  # type: ignore
from hex.hex_grid import HexGrid  # Reaproveita métodos de desenho
from utils.p5_utils import draw_vertex, draw_map


# ------------------ Parâmetros da grade ------------------ #
HEX_SIZE = 64  # raio (distância centro->vértice)
INITIAL_WIDTH = 1200
INITIAL_HEIGHT = 900
dyn_cols = 0  # calculado dinamicamente
dyn_rows = 0  # calculado dinamicamente
UI_PANEL_HEIGHT = 230  # altura reservada para painel de ajuda (ajustado para novas linhas)
UI_TITLE_SIZE = 20
UI_ENTRY_SIZE = 14
fit_to_area = True  # escala grade para preencher área disponível
last_scale = 1.0  # escala calculada no frame


# ------------------ Estado ------------------ #
grid: HexGrid | None = None
tile_edges: list[list[list[int]]] = []  # [row][col][6]
show_help = True
hover_cell: tuple[int, int] | None = None
INNER_MIN = 0.05
INNER_MAX = 0.9
INNER_STEP = 0.05
debug_edges = False
show_empty_hex = True  # controla exibição dos hex vazios (brancos)
hide_inner_when_empty = True  # oculta cubo interno em células sem bordas
BASE_EDGE_PALETTE: list[str] | None = None  # paleta original das barras
EDGE_PALETTES: list[list[str]] = []
INNER_PALETTES: list[list[str]] = [
    ["#222222", "#555555", "#999999"],
    ["#2b2d42", "#8d99ae", "#edf2f4"],
    ["#264653", "#2a9d8f", "#e9c46a"],
]
current_edge_palette_index = 0
current_inner_palette_index = 0


def _random_palette() -> list[str]:
    return [f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}" for _ in range(3)]

def randomize_edges_only():
    if grid:
        pal = _random_palette()
        grid.colors = pal  # type: ignore

def randomize_inner_only():
    if grid:
        pal = _random_palette()
        grid.inner_colors = pal  # type: ignore
def init_state():
    global tile_edges, dyn_cols, dyn_rows
    if dyn_cols > 0 and dyn_rows > 0:
        tile_edges = [[[0 for _ in range(6)] for _ in range(dyn_cols)] for _ in range(dyn_rows)]
    else:
        tile_edges = []

def ensure_layout():
    """Recalcula dyn_cols/dyn_rows conforme área disponível e ajusta tile_edges preservando dados."""
    global dyn_cols, dyn_rows, tile_edges, grid
    avail_w = py5.width
    avail_h = py5.height - UI_PANEL_HEIGHT
    hex_height = math.sin(math.pi * 2 / 6) * HEX_SIZE * 2
    hex_width = HEX_SIZE * 1.5
    # margem lateral = HEX_SIZE
    new_cols = max(1, int((avail_w - HEX_SIZE * 1) // hex_width))
    new_rows = max(1, int(((avail_h - HEX_SIZE * 1) // hex_height)))
    if new_cols == dyn_cols and new_rows == dyn_rows and tile_edges:
        return
    # construir nova matriz preservando sobreposição
    old_edges = tile_edges
    new_edges = [[[0 for _ in range(6)] for _ in range(new_cols)] for _ in range(new_rows)]
    for r in range(min(dyn_rows, new_rows)):
        for c in range(min(dyn_cols, new_cols)):
            if r < len(old_edges) and c < len(old_edges[0]):
                new_edges[r][c] = old_edges[r][c]
    dyn_cols, dyn_rows = new_cols, new_rows
    tile_edges = new_edges
    # preservar estado visual do grid anterior
    prev_inner_scale = None
    prev_inner_colors = None
    if grid is not None:
        try:
            prev_inner_scale = grid.inner_scale
            prev_inner_colors = list(grid.inner_colors) if grid.inner_colors else None
        except Exception:
            pass
    # recria grid para refletir novo tamanho
    grid = HexGrid(cols=dyn_cols, rows=dyn_rows, size=HEX_SIZE, draw_vertex=draw_vertex, draw_map=draw_map)
    if prev_inner_scale is not None:
        grid.inner_scale = prev_inner_scale  # type: ignore
    if prev_inner_colors is not None:
        grid.inner_colors = prev_inner_colors  # type: ignore


def cell_center(row: int, col: int):
    # Repete lógica de HexGrid para evitar confusões de nomes
    hex_height = math.sin(math.pi * 2 / 6) * HEX_SIZE * 2
    hex_width = HEX_SIZE * 1.5
    offset = HEX_SIZE
    offset_y = hex_height / 2 if col % 2 == 1 else 0
    x = col * hex_width + offset
    y = row * hex_height + offset_y + offset
    return x, y


def get_cell_at(x: float, y: float):
    hex_height = math.sin(math.pi * 2 / 6) * HEX_SIZE * 2
    hex_width = HEX_SIZE * 1.5
    col = int(x // hex_width)
    row = int((y - (col % 2) * hex_height / 2) // hex_height)
    if 0 <= col < dyn_cols and 0 <= row < dyn_rows:
        return row, col
    return -1, -1


def edge_midpoints(row: int, col: int):
    cx, cy = cell_center(row, col)
    vertices = []
    for i in range(6):
        ang = math.pi * 2 / 6 * i
        vx = cx + math.cos(ang) * HEX_SIZE
        vy = cy + math.sin(ang) * HEX_SIZE
        vertices.append((vx, vy))
    mids = []
    for i in range(6):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % 6]
        mids.append(((v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2))
    return mids, vertices


def nearest_edge_index(row: int, col: int, mx: float, my: float):
    mids, _ = edge_midpoints(row, col)
    best_i, best_d = -1, 1e9
    for i, (ex, ey) in enumerate(mids):
        d = (ex - mx) ** 2 + (ey - my) ** 2
        if d < best_d:
            best_d = d
            best_i = i
    return best_i


def draw_hover_edge_indicator(row: int, col: int, mx: float, my: float):
    """Desenha um pequeno triângulo vermelho apontando para a borda a ser alternada."""
    edge_i = nearest_edge_index(row, col, mx, my)
    if edge_i < 0:
        return
    mids, vertices = edge_midpoints(row, col)
    midx, midy = mids[edge_i]
    cx, cy = cell_center(row, col)
    # Vetor direção centro->meio borda
    dx = midx - cx
    dy = midy - cy
    dist = max((dx * dx + dy * dy) ** 0.5, 1e-6)
    ux, uy = dx / dist, dy / dist
    # Parâmetros geométricos do triângulo
    apex_len = HEX_SIZE * 0.20
    inset = HEX_SIZE * 0.06
    half_w = HEX_SIZE * 0.07
    # Pontos
    base_cx = midx - ux * inset
    base_cy = midy - uy * inset
    apex_x = midx + ux * apex_len
    apex_y = midy + uy * apex_len
    # Perpendicular
    px, py = -uy, ux
    left_x = base_cx + px * half_w
    left_y = base_cy + py * half_w
    right_x = base_cx - px * half_w
    right_y = base_cy - py * half_w
    # Desenho
    py5.no_stroke()
    py5.fill(255, 0, 0, 200)
    py5.begin_shape()
    py5.vertex(apex_x, apex_y)
    py5.vertex(left_x, left_y)
    py5.vertex(right_x, right_y)
    py5.end_shape(py5.CLOSE)
    return edge_i


def toggle_edge(row: int, col: int, edge_i: int, value: int | None = None):
    if not (0 <= row < dyn_rows and 0 <= col < dyn_cols and 0 <= edge_i < 6):
        return
    cur = tile_edges[row][col][edge_i]
    tile_edges[row][col][edge_i] = (1 - cur) if value is None else value


def clear_cell(row: int, col: int):
    if 0 <= row < dyn_rows and 0 <= col < dyn_cols:
        tile_edges[row][col] = [0] * 6


def fill_cell(row: int, col: int):
    if 0 <= row < dyn_rows and 0 <= col < dyn_cols:
        tile_edges[row][col] = [1] * 6


def export_unique_tiles():
    patterns = set()
    for r in range(dyn_rows):
        for c in range(dyn_cols):
            edges = tuple(tile_edges[r][c])
            if any(edges):  # ignora vazios
                patterns.add(edges)
    tiles = [dict(id=i, edges=list(p)) for i, p in enumerate(sorted(patterns))]
    out_path = Path(__file__).parent / "tiles.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(tiles, f, ensure_ascii=False, indent=2)
    print(f"Exportados {len(tiles)} padrões para {out_path}")
    return tiles


# ------------------ Desenho das conexões (reuso estilo) ------------------ #
# Arestas classificadas: {1,3,5} desenhadas antes (atrás do cubo interno), {0,2,4} depois (frente)
BACK_EDGE_INDICES = {1, 3, 5}   # “quinas” atrás
FRONT_EDGE_INDICES = {0, 2, 4}  # frente


def draw_edges(row: int, col: int, phase: str):
    edges = tile_edges[row][col]
    if not any(edges):
        return
    order = [3, 5, 1, 2, 4, 0]
    mapping = [4, -1, 0, 1, 2, 3]
    cx, cy = cell_center(row, col)
    size = HEX_SIZE
    for i in order:
        if edges[i] != 1:
            continue
        is_back = i in BACK_EDGE_INDICES
        if phase == 'back' and not is_back:
            continue
        if phase == 'front' and is_back:
            continue
        idx = mapping[i] + 2
        ang1 = math.pi * 2 / 6 * idx
        ang2 = math.pi * 2 / 6 * ((idx + 1) % 6)
        v1x = cx + math.cos(ang1) * size
        v1y = cy + math.sin(ang1) * size
        v2x = cx + math.cos(ang2) * size
        v2y = cy + math.sin(ang2) * size
        ex = (v1x + v2x) / 2
        ey = (v1y + v2y) / 2
        color_groups = [[3, 4, 6, 7], [1, 2, 10, 11], [0, 5, 8, 9]]
        c1 = grid.colors[2] if (i + 6) in color_groups[0] else grid.colors[0] if (i + 6) in color_groups[1] else grid.colors[1]  # type: ignore
        c2 = grid.colors[2] if i in color_groups[0] else grid.colors[0] if i in color_groups[1] else grid.colors[1]  # type: ignore
        inner = grid.inner_scale if grid else 0.29  # type: ignore
        t = max(0.0, (inner - 0.30) / (0.90 - 0.30))
        start_offset = size * 0.40 * min(1.0, t)
        grid.draw_parallel_shapes(cx, cy, ex, ey, [c1, c2], start_offset=start_offset)  # type: ignore

        # Rótulo de índice para depuração (desenha só na fase front para evitar duplicar)
        if debug_edges and phase == 'front':
            py5.push_style()
            py5.fill(0)
            py5.text_align(py5.CENTER, py5.CENTER)
            py5.text(str(i), ex, ey)
            py5.pop_style()


def draw_help_panel():
    # painel de fundo
    py5.no_stroke()
    py5.fill(32, 32, 32, 245)
    py5.rect(0, 0, py5.width, UI_PANEL_HEIGHT)
    py5.stroke(0)
    py5.stroke_weight(1)
    py5.line(0, UI_PANEL_HEIGHT - 1, py5.width, UI_PANEL_HEIGHT - 1)
    py5.fill(255)
    py5.text_align(py5.LEFT, py5.TOP)
    py5.text_leading(16)

    # título
    py5.text_size(UI_TITLE_SIZE)
    py5.text("Ajuda (H para ocultar)", 12, 8)
    # linha status célula abaixo do título
    py5.text_size(UI_ENTRY_SIZE - 2)
    if hover_cell:
        r, c = hover_cell
        edges = tile_edges[r][c]
        py5.fill(200)
        py5.text(f"Célula r={r} c={c} edges={edges}", 12, 30)
        py5.fill(255)

    if not show_help:
        py5.text("(H) mostrar ajuda", 12, UI_PANEL_HEIGHT - 24)
        return

    inner_val = f"{grid.inner_scale:.2f}" if grid else "--"
    debug_line = "ON" if debug_edges else "OFF"

    entries = [
        ("Mouse ESQ", "Alterna borda"),
        ("SHIFT+ESQ", "Liga todas"),
        ("CTRL+ESQ", "Desliga todas"),
        ("DIR", "Limpa célula"),
        ("S", "Salvar tiles.json"),
        ("R", "Reset grade"),
        ("C", "Copiar padrão célula"),
        ("+  /  -", f"Inner {inner_val}"),
    ("1 2 3", "Paletas ambos"),
    ("0", "Reset ambos"),
    ("X", "Aleatória ambos"),
    ("B", "Ciclar barras"),
    ("U", "Ciclar cubo"),
    ("P", "Aleatória barras"),
    ("O", "Aleatória cubo"),
        ("G", f"Debug {debug_line}"),
        ("V", "Mostrar/ocultar vazios"),
        ("I", f"Inner vazios {'OFF' if hide_inner_when_empty else 'ON'}"),
    ("F", f"Fit {'ON' if fit_to_area else 'OFF'}"),
        ("H", "Ocultar painel"),
    ]

    # Botão toggle mostrar vazios
    global show_empty_hex
    btn_w, btn_h = 160, 26
    btn_x = py5.width - btn_w - 16
    btn_y = 12
    py5.fill(70, 70, 70)
    py5.rect(btn_x, btn_y, btn_w, btn_h, 4)
    py5.fill(220)
    py5.text_align(py5.CENTER, py5.CENTER)
    label = "Ocultar hex vazios" if show_empty_hex else "Mostrar hex vazios"
    py5.text_size(12)
    py5.text(label, btn_x + btn_w / 2, btn_y + btn_h / 2)
    py5.text_align(py5.LEFT, py5.TOP)
    py5.text_size(UI_ENTRY_SIZE)
    # Guardar área do botão em globals simples
    global _btn_bounds
    _btn_bounds = (btn_x, btn_y, btn_w, btn_h)

    # duas colunas
    py5.text_size(UI_ENTRY_SIZE)
    col_w = 150
    first_col_x = 12
    second_col_x = 12 + col_w + 180
    y0 = 52
    line_h = UI_ENTRY_SIZE + 2
    half = (len(entries) + 1) // 2
    for i, (cmd, desc) in enumerate(entries):
        if i < half:
            x_cmd = first_col_x
            y = y0 + i * line_h
        else:
            x_cmd = second_col_x
            y = y0 + (i - half) * line_h
        py5.fill(210)
        py5.text(cmd, x_cmd, y)
        py5.fill(255)
        py5.text(desc, x_cmd + 120, y)

# ------------------ py5 lifecycle ------------------ #
def settings():  # tamanho dinâmico baseado na grade
    hex_height = math.sin(math.pi * 2 / 6) * HEX_SIZE * 2
    hex_width = HEX_SIZE * 1.5
    # Usa valores provisórios se dinâmicos ainda não calculados
    cols = dyn_cols if dyn_cols else 10
    rows = dyn_rows if dyn_rows else 6
    w = int(cols * hex_width + HEX_SIZE * 2)
    h = int((rows + 0.5) * hex_height + HEX_SIZE * 2 + UI_PANEL_HEIGHT)
    py5.size(w, h)


def _grid_dimensions():
    hex_height = math.sin(math.pi * 2 / 6) * HEX_SIZE * 2
    hex_width = HEX_SIZE * 1.5
    grid_w = dyn_cols * hex_width + HEX_SIZE * 2
    grid_h = (dyn_rows + 0.5) * hex_height + HEX_SIZE * 2
    return grid_w, grid_h


def setup():
    global grid
    py5.frame_rate(60)
    init_state()
    global BASE_EDGE_PALETTE
    if BASE_EDGE_PALETTE is None and grid is not None:
        BASE_EDGE_PALETTE = list(grid.colors)
    ensure_layout()
    grid = HexGrid(
        cols=dyn_cols, rows=dyn_rows, size=HEX_SIZE, draw_vertex=draw_vertex, draw_map=draw_map
    )
    # Inicializa paletas se vazio
    global EDGE_PALETTES, current_edge_palette_index, current_inner_palette_index
    if not EDGE_PALETTES:
        EDGE_PALETTES = [
            list(grid.colors),
            ["#666666", "#999999", "#333333"],
            ["#1b263b", "#415a77", "#0d1b2a"],
            ["#2f4858", "#86bbd8", "#1b3a4b"],
        ]
    current_edge_palette_index = 0
    current_inner_palette_index = 0
    # Título da janela (ignora caso não suportado nesta versão do py5)
    try:
        # Algumas versões expõem 'surface', outras requerem py5.get_surface()
        if hasattr(py5, "surface") and hasattr(py5.surface, "set_title"):
            py5.surface.set_title("Gerador Ladrilhos Hexagonais - Interativo")
        elif hasattr(py5, "get_surface"):
            surf = py5.get_surface()
            if hasattr(surf, "set_title"):
                surf.set_title("Gerador Ladrilhos Hexagonais - Interativo")
    except Exception:
        pass
    print(__doc__)


def draw():
    py5.background(240)
    ensure_layout()
    # Painel
    draw_help_panel()
    # Desenho da grade deslocado para baixo
    py5.push_matrix()
    py5.translate(0, UI_PANEL_HEIGHT)
    grid_w, grid_h = _grid_dimensions()
    avail_w = py5.width
    avail_h = py5.height - UI_PANEL_HEIGHT
    scale_factor = 1.0
    if fit_to_area:
        scale_factor = min(avail_w / grid_w, avail_h / grid_h)
    global last_scale
    last_scale = scale_factor
    if scale_factor != 1.0:
        # Centraliza horizontal e verticalmente dentro da área disponível
        offset_x = (avail_w - grid_w * scale_factor) / 2
        offset_y = (avail_h - grid_h * scale_factor) / 2
        py5.translate(offset_x, offset_y)
        py5.scale(scale_factor)
    # Borda da área desenhável
    py5.no_fill()
    py5.stroke(0, 80)
    py5.stroke_weight(2)
    py5.rect(0, 0, grid_w, grid_h)
    # Base (hex externo). Quando show_empty_hex==False não desenha NENHUM contorno.
    if show_empty_hex:
        grid.draw_base()
    for r in range(dyn_rows):
        for c in range(dyn_cols):
            draw_edges(r, c, phase='back')
    # Inner (cubo) com regras
    for r in range(dyn_rows):
        for c in range(dyn_cols):
            edges_active = any(tile_edges[r][c])
            if not show_empty_hex and not edges_active:
                continue  # totalmente oculto
            if hide_inner_when_empty and not edges_active:
                continue  # pula inner só se vazio
            cx, cy = cell_center(r, c)
            inner = max(0.02, min(0.95, grid.inner_scale))  # type: ignore
            palette = grid.inner_colors if grid.inner_colors else grid.colors  # type: ignore
            grid.draw_hexagon(cx, cy, HEX_SIZE * inner, math.pi * 2 / 12, palette)  # type: ignore
    if hover_cell and all(0 <= v for v in hover_cell):
        r, c = hover_cell
        cx, cy = cell_center(r, c)
        py5.no_fill()
        py5.stroke(0, 120)
        py5.stroke_weight(2)
        vertices = []
        for i in range(6):
            ang = math.pi * 2 / 6 * i
            vertices.append((cx + math.cos(ang) * HEX_SIZE, cy + math.sin(ang) * HEX_SIZE))
        py5.begin_shape()
        for vx, vy in vertices:
            py5.vertex(vx, vy)
        py5.end_shape(py5.CLOSE)
        draw_hover_edge_indicator(r, c, py5.mouse_x, py5.mouse_y - UI_PANEL_HEIGHT)
    for r in range(dyn_rows):
        for c in range(dyn_cols):
            draw_edges(r, c, phase='front')
    py5.pop_matrix()


def mouse_moved():  # atualizar célula sob o mouse
    global hover_cell
    if py5.mouse_y < UI_PANEL_HEIGHT:
        hover_cell = None
        return
    # remover offset de centralização e escala
    mx = py5.mouse_x
    my = py5.mouse_y - UI_PANEL_HEIGHT
    grid_w, grid_h = _grid_dimensions()
    avail_w = py5.width
    avail_h = py5.height - UI_PANEL_HEIGHT
    if fit_to_area and last_scale != 0:
        offset_x = (avail_w - grid_w * last_scale) / 2
        offset_y = (avail_h - grid_h * last_scale) / 2
        mx = (mx - offset_x)
        my = (my - offset_y)
        mx /= last_scale
        my /= last_scale
    r, c = get_cell_at(mx, my)
    hover_cell = (r, c) if r >= 0 else None


def mouse_pressed():
    if py5.mouse_button == py5.LEFT:
        if py5.mouse_y < UI_PANEL_HEIGHT:
            return
        mx = py5.mouse_x
        my = py5.mouse_y - UI_PANEL_HEIGHT
        grid_w, grid_h = _grid_dimensions()
        avail_w = py5.width
        avail_h = py5.height - UI_PANEL_HEIGHT
        if fit_to_area and last_scale != 0:
            offset_x = (avail_w - grid_w * last_scale) / 2
            offset_y = (avail_h - grid_h * last_scale) / 2
            mx = (mx - offset_x)
            my = (my - offset_y)
            mx /= last_scale
            my /= last_scale
        r, c = get_cell_at(mx, my)
        if r < 0:
            return
        if py5.is_key_pressed and py5.key_code == py5.SHIFT:
            fill_cell(r, c)
            return
        if py5.is_key_pressed and py5.key_code == py5.CONTROL:
            clear_cell(r, c)
            return
        edge_i = nearest_edge_index(r, c, mx, my)
        toggle_edge(r, c, edge_i)
    elif py5.mouse_button == py5.RIGHT:
        if py5.mouse_y < UI_PANEL_HEIGHT:
            return
        mx = py5.mouse_x
        my = py5.mouse_y - UI_PANEL_HEIGHT
        grid_w, grid_h = _grid_dimensions()
        avail_w = py5.width
        avail_h = py5.height - UI_PANEL_HEIGHT
        if fit_to_area and last_scale != 0:
            offset_x = (avail_w - grid_w * last_scale) / 2
            offset_y = (avail_h - grid_h * last_scale) / 2
            mx = (mx - offset_x)
            my = (my - offset_y)
            mx /= last_scale
            my /= last_scale
        r, c = get_cell_at(mx, my)
        clear_cell(r, c)
    # clique em botão do painel
    if py5.mouse_y < UI_PANEL_HEIGHT and py5.mouse_button == py5.LEFT:
        if '_btn_bounds' in globals():
            bx, by, bw, bh = _btn_bounds
            if bx <= py5.mouse_x <= bx + bw and by <= py5.mouse_y <= by + bh:
                global show_empty_hex
                show_empty_hex = not show_empty_hex


def key_pressed():
    global show_help
    if py5.key in ("s", "S"):
        export_unique_tiles()
    elif py5.key in ("r", "R"):
        init_state()
    elif py5.key in ("h", "H"):
        show_help = not show_help
    elif py5.key in ("c", "C") and hover_cell and hover_cell[0] >= 0:
        r, c = hover_cell
        print(f"Padrão célula (r={r}, c={c}): {tile_edges[r][c]}")
    elif py5.key in ('+', '=') and grid:
        grid.inner_scale = min(INNER_MAX, grid.inner_scale + INNER_STEP)
    elif py5.key in ('-', '_') and grid:
        grid.inner_scale = max(INNER_MIN, grid.inner_scale - INNER_STEP)
    elif py5.key == '1' and grid:
        grid.inner_colors = ["#222222", "#555555", "#999999"]
        grid.colors = ["#666666", "#999999", "#333333"]
    elif py5.key == '2' and grid:
        grid.inner_colors = ["#2b2d42", "#8d99ae", "#edf2f4"]
        grid.colors = ["#1b263b", "#415a77", "#0d1b2a"]
    elif py5.key == '3' and grid:
        grid.inner_colors = ["#264653", "#2a9d8f", "#e9c46a"]
        grid.colors = ["#2f4858", "#86bbd8", "#1b3a4b"]
    elif py5.key == '0' and grid:
        if BASE_EDGE_PALETTE:
            grid.colors = list(BASE_EDGE_PALETTE)
        grid.inner_colors = list(grid.colors)
    elif py5.key in ('x', 'X') and grid:
        def rand_color():
            return f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}"
        pal = [rand_color() for _ in range(3)]
        grid.inner_colors = list(pal)
        grid.colors = list(pal)
    elif py5.key in ('b','B') and grid:
        global current_edge_palette_index
        if EDGE_PALETTES:
            current_edge_palette_index = (current_edge_palette_index + 1) % len(EDGE_PALETTES)
            grid.colors = list(EDGE_PALETTES[current_edge_palette_index])
    elif py5.key in ('u','U') and grid:
        global current_inner_palette_index
        if INNER_PALETTES:
            current_inner_palette_index = (current_inner_palette_index + 1) % len(INNER_PALETTES)
            grid.inner_colors = list(INNER_PALETTES[current_inner_palette_index])
    elif py5.key in ('p','P') and grid:
        randomize_edges_only()
    elif py5.key in ('o','O') and grid:
        randomize_inner_only()
    elif py5.key in ('g', 'G'):
        global debug_edges
        debug_edges = not debug_edges
    elif py5.key in ('v', 'V'):
        global show_empty_hex
        show_empty_hex = not show_empty_hex
    elif py5.key in ('i', 'I'):
        global hide_inner_when_empty
        hide_inner_when_empty = not hide_inner_when_empty
    elif py5.key in ('f', 'F'):
        global fit_to_area
        fit_to_area = not fit_to_area


py5.run_sketch(block=False)
