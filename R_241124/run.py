import sys
import random
import py5

from utils.image_utils import save_frames, create_gif

if len(sys.argv) > 1:
    seed = int(sys.argv[1])
else:
    seed = random.randint(0, 10000)

# Variáveis globais para armazenar os ângulos de rotação
angle_x = 0
angle_y = 0
prev_mouse_x = 0
prev_mouse_y = 0

def settings():
    size = 750
    py5.size(size , size, py5.P3D)  # Defina o tamanho da tela e o modo 3D

def setup():
    global hex_grid, prev_mouse_x, prev_mouse_y
    random.seed(seed)
    py5.no_fill()
    py5.stroke(255)
    prev_mouse_x = py5.mouse_x
    prev_mouse_y = py5.mouse_y

def draw():
    global angle_x, angle_y, prev_mouse_x, prev_mouse_y

    py5.background(0)
    py5.translate(py5.width / 2, py5.height / 2, 0)
    
    # Atualiza os ângulos de rotação com base no movimento do mouse
    angle_x += (py5.mouse_y - prev_mouse_y) * 0.01
    angle_y += (py5.mouse_x - prev_mouse_x) * 0.01
    prev_mouse_x = py5.mouse_x
    prev_mouse_y = py5.mouse_y
    
    # Aplica as rotações
    py5.rotate_x(angle_x)
    py5.rotate_y(angle_y)
    
    # Desenha o cubo estático
    py5.box(200)  # Desenha o cubo

    # Desenha os paralelepípedos
    py5.stroke_weight(1)
    
    # Paralelepípedo no eixo X
    py5.push_matrix()
    py5.translate(0, 0, 0)
    py5.box(600, 50, 50)
    py5.pop_matrix()
    
    # Paralelepípedo no eixo Y
    py5.push_matrix()
    py5.translate(0, 0, 0)
    py5.rotate_z(py5.HALF_PI)
    py5.box(600, 50, 50)
    py5.pop_matrix()
    
    # Paralelepípedo no eixo Z
    py5.push_matrix()
    py5.translate(0, 0, 0)
    py5.rotate_y(py5.HALF_PI)
    py5.box(600, 50, 50)
    py5.pop_matrix()

def key_pressed():
    global seed, frames_dir
    if py5.key == 's' or py5.key == 'S':
        create_gif(frames_dir, seed)
    if py5.key == 'r' or py5.key == 'R':
        frames_dir = save_frames(seed, limit=50, start=0)

py5.run_sketch(block=False)