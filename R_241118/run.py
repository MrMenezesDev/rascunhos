import py5

from hex.hex_grid import HexGrid
from utils.p5_utils import draw_map, draw_vertex
from hex.hex_wave_collapse import HexWaveFunctionCollapseGrid

hex_grid = None


def settings():
    py5.size(512 + 256, 512)  # Defina o tamanho da tela


def setup():
    global hex_grid
    col = 10
    row = 5
    grid = HexGrid(cols=col, rows=row, size=50, draw_vertex=draw_vertex, draw_map=draw_map)
    grid.draw()
    hex_grid = HexWaveFunctionCollapseGrid(
        dim=[col, row], draw_cell=grid.draw_cell, border=True
    )
    hex_grid.start()


def draw():
    global hex_grid
    hex_grid.collapse()
    hex_grid.draw()
    if hex_grid.complete:
        py5.no_loop()

py5.run_sketch()

