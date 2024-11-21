import sys
import random
import py5

from zen.zen_utils import draw_spiral_poligono
from utils.image_utils import save_frames, create_gif
from zen.zentangle import Layout, Zentangle


size = 976
if len(sys.argv) > 1:
    seed = int(sys.argv[1])
else:
    seed = random.randint(0, 10000)


def settings():
    global size
    py5.size(size, size)  # Defina o tamanho da tela

layout = None
current_factor = 0.6
factor_direction = 1
side = {}

def rule(zen: Zentangle, action: str, kargs):
    global current_factor, factor_direction
    col, line = kargs["col"], kargs["line"]
    if action == "animate":
        # Espaçamento duplo no início
        initial_spacing = zen.spacing * 2

        py5.square(
            (col * (zen.width + zen.spacing)) + initial_spacing,
            (line * (zen.height + zen.spacing)) + initial_spacing,
            zen.width,
        )

        draw_spiral_poligono(
            side[col, line],
            col,
            line,
            zen,
            initial_spacing,
            py5.line,
            factor=current_factor,
        )

        # Atualizar o fator
        initial_factor = 0.4
        max_factor = initial_factor * 4
        increment = initial_factor / 4

        current_factor += increment * factor_direction
        if current_factor >= max_factor or current_factor <= initial_factor:
            factor_direction *= -1

    elif action == "draw":
        # Add border to the zentangle
        py5.stroke(zen.border_color)
        py5.stroke_weight(zen.border_size)

        # Define a cor de fundo do quadrado
        py5.fill(zen.background_color)

        # Espaçamento duplo no início
        initial_spacing = zen.spacing * 2

        py5.square(
            (col * (zen.width + zen.spacing)) + initial_spacing,
            (line * (zen.height + zen.spacing)) + initial_spacing,
            zen.width,
        )

        draw_spiral_poligono(
            side[col, line],
            col,
            line,
            zen,
            initial_spacing,
            py5.line,
            factor=current_factor,
        )


def setup():
    global seed, size, layout
    random.seed(seed)
    layout = Layout(height=size, width=size)
    for col in range(7):
        for line in range(7):
            side[(col, line)] = random.randint(3, 6)  # Example initialization
    for _ in range(7 * 7):
        layout.add_zentangle(Zentangle(height=128, width=128, rule=rule))
    layout.draw_grid()


def draw():
    global layout

    # Control FPS
    py5.frame_rate(10)

    layout.animate_grid()


def key_pressed():
    global seed, frames_dir, layout
    if py5.key == "s" or py5.key == "S":
        create_gif(frames_dir, seed)
    if py5.key == "r" or py5.key == "R":
        frames_dir = save_frames(seed, limit=50, start=0)


py5.run_sketch(block=False)
