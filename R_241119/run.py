import sys
import random
import py5

from utils.image_utils import save_frames, create_gif
from utils.p5_utils import draw_map, draw_vertex
from hex.hex_grid import HexGrid

hex_grid = None
if len(sys.argv) > 1:
    seed = int(sys.argv[1])
else:
    seed = random.randint(0, 10000)
import time
import py5
from eca.eca import ECA

# Variáveis globais
hex_grid = None
eca = None

def settings():
    """
    Configura o tamanho da janela.
    """
    py5.size(800, 800)

def setup():
    """
    Configura o ambiente inicial do sketch.
    """
    global hex_grid, eca
    start_time = time.time()
    py5.background(255)
    hex_grid = HexGrid(50, 50, 10, draw_vertex, draw_map)  # Inicialize hex_grid aqui
    eca = ECA()
    eca.start()
    end_time = time.time()
    print(f"setup function took {end_time - start_time:.4f} seconds")

def draw():
    """
    Função de desenho chamada repetidamente pelo py5.
    """
    start_time = time.time()
    global eca
    py5.background(255)
    if eca.evolution_history:
        hex_grid.set_state(eca.evolution_history, eca.step)
        hex_grid.draw()
        eca.step += eca.direction
        if eca.step == len(eca.evolution_history) - 1:
            eca.direction = -1
            print("Starting evolution in a separate thread")
            # eca.start(update=False)
        elif eca.step == 0:
            eca.direction = 1
            py5.no_loop()
            # eca.plot_evolution()
    end_time = time.time()
    print(f"draw function took {end_time - start_time:.4f} seconds")

def key_pressed():
    global seed, frames_dir
    if py5.key == 's' or py5.key == 'S':
        create_gif(frames_dir, seed)


frames_dir = save_frames(seed, limit=None, start=0)
py5.run_sketch(block=False)