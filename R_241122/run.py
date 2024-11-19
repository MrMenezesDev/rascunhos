import sys
import numpy as np
import py5
from maze.maze import generate_random3_d_grid
from utils.image_utils import create_gif, save_frames
from utils.p5_utils import draw_line_between_points, draw_sphere_at_point

class ColorManager:
    def __init__(self):
        self.sphere_start = (255, 0, 255)  # Neon Pink
        self.sphere_end = (0, 255, 255)  # Neon Cyan
        self.sphere_interpolated = (255, 255, 0)  # Neon Yellow
        self.cube = (0, 255, 255, 64)  # Neon Cyan com alpha
        self.background = (0, 0, 64)  # Azul Escuro
        self.lines = (255, 0, 255)  # Neon Pink

color_manager = ColorManager()

base_box = 200
pontos = 30
matriz = generate_random3_d_grid(base_box, pontos)
zoom = 0

current_position_index = 0  # Índice da posição atual da esfera
frame_counter = 0  # Contador de frames
frame_delay = 0  # Número de frames a esperar antes de atualizar a posição
interpolation_factor = 10  # Fator de interpolação
speed = 5  # Velocidade da esfera

def setup():
    py5.size(600, 600, py5.P3D)
    py5.loop()

def draw():
    global base_box, matriz, zoom, rotate_x_angle, rotate_y_angle, auto_move, current_position_index, frame_counter, interpolation_factor, speed
    py5.background(*color_manager.background)
    py5.lights()
    py5.no_fill()
    py5.translate(py5.width / 2, py5.height / 2, zoom)
    
    if auto_move:
        py5.rotate_x(py5.radians(rotate_x_angle))
        py5.rotate_y(py5.radians(rotate_y_angle)) 
    else:
        py5.rotate_x(py5.radians(py5.mouse_y))
        py5.rotate_y(py5.radians(py5.mouse_x))
    
    py5.stroke(*color_manager.cube)
    py5.box(base_box)
    py5.stroke_weight(2)
    py5.stroke(*color_manager.lines)
    for i in range(len(matriz) - 1):
        draw_line_between_points(matriz[i], matriz[i + 1], base_box)
    draw_sphere_at_point(matriz[0], color_manager.sphere_start, base_box, size=5)
    draw_sphere_at_point(matriz[-1], color_manager.sphere_end, base_box, size=5)
    
    # Calcule a posição interpolada da esfera
    p1 = matriz[current_position_index]
    p2 = matriz[(current_position_index + 1) % len(matriz)]
    distance = np.linalg.norm(np.array(p2) - np.array(p1))
    interpolated_position = [
        p1[0] + (p2[0] - p1[0]) * interpolation_factor,
        p1[1] + (p2[1] - p1[1]) * interpolation_factor,
        p1[2] + (p2[2] - p1[2]) * interpolation_factor
    ]
    
    # Desenhe a esfera na posição interpolada
    draw_sphere_at_point(interpolated_position, color_manager.sphere_interpolated, base_box, size=10)
    
    # Atualize a interpolação e a posição da esfera
    frame_counter += 1
    if frame_counter >= frame_delay:
        frame_counter = 0
        interpolation_factor += speed / distance
        if interpolation_factor >= 1:
            interpolation_factor = 0
            current_position_index = (current_position_index + 1) % len(matriz)

def mouse_moved():
    py5.redraw()

def mouse_wheel(e):
    global zoom
    zoom += e.get_count() * 10
    py5.redraw()

def key_pressed():
    global seed, frames_dir, auto_move
    if py5.key == 's' or py5.key == 'S':
        frames_dir = save_frames(seed, limit=0, start=0)
    if py5.key == 'z' or py5.key == 'Z':
        create_gif(frames_dir, seed, infinite_loop=True)
    if py5.key == 'a' or py5.key == 'A':
        auto_move = not auto_move
 
if len(sys.argv) > 1:
    seed = int(sys.argv[1])
else:
    seed = 42  # Valor padrão para a seed

np.random.seed(seed)
       
py5.run_sketch(block=False)

rotate_x_angle = 0
rotate_y_angle = 0
angle = 0
auto_move = True

while True:
    import time
    angle += 0.01
    rotate_x_angle += 5 * py5.sin(angle)
    rotate_y_angle += 5 * py5.cos(angle)
    
    time.sleep(0.1)
    py5.redraw()