import sys
import random
import py5

from utils.image_utils import save_frames, create_gif
from utils.p5_utils import draw_map, draw_vertex
from hex.hex_grid import HexGrid
from hex.hex_wave_collapse import HexWaveFunctionCollapseGrid

hex_grid = None
if len(sys.argv) > 1:
    seed = int(sys.argv[1])
else:
    seed = random.randint(0, 10000)

def settings():
    size = 768
    py5.size(int(size * 1.5) , size)  # Defina o tamanho da tela

def setup():
    global hex_grid
    random.seed(seed)
    col = 15
    row = 8
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

def key_pressed():
    global seed, frames_dir
    if py5.key == 's' or py5.key == 'S':
        create_gif(frames_dir, seed)


frames_dir = save_frames(seed, limit=None, start=0)
py5.run_sketch(block=False)