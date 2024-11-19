import py5
import numpy as np
import sys

from utils.image_utils import save_frames, create_gif
from maze.maze import generate_matrix

# Adicionar a lógica para definir a seed
if len(sys.argv) > 1:
    seed = int(sys.argv[1])
else:
    seed = 42  # Valor padrão para a seed

np.random.seed(seed)

def generate_cube(base, size):
    cantos_base = []
    cantos_topo = []
    arestas = []

    # Gerar os 8 vértices do cubo

    # Vértices da base
    cantos_base.append([0, 0, 0])
    cantos_base.append([base, 0, 0])
    cantos_base.append([base, base, 0])
    cantos_base.append([0, base, 0])

    # Vértices do topo
    cantos_topo.append([0, 0, base])
    cantos_topo.append([base, 0, base])
    cantos_topo.append([base, base, base])
    cantos_topo.append([0, base, base])

    # Arestas da base
    for i in range(4):
        arestas.append([cantos_base[i], cantos_base[(i + 1) % 4]])

    # Arestas do topo
    for i in range(4):
        arestas.append([cantos_topo[i], cantos_topo[(i + 1) % 4]])

    # Arestas verticais
    for i in range(4):
        arestas.append([cantos_base[i], cantos_topo[i]])

    return cantos_base, cantos_topo, arestas


def settings():
    """
    Configura o tamanho da janela.
    """
    py5.size(800, 800, py5.P3D)


def setup():
    """
    Configura o ambiente inicial do sketch.
    """
    py5.background(255)
    py5.no_loop()


def draw():
    global cubo, matriz, base, face
    """
    Função de desenho chamada repetidamente pelo py5.
    """
    global rotate_x_angle, rotate_y_angle, angle
    print(rotate_speed, rotate_x_angle, rotate_y_angle)
    # # Simular interpolação de um ponto para outro da tela com o mouse

    py5.background(255)

    cantos_base, cantos_topo, cube_edges = cubo

    # Calcular o centro do cubo
    center_x = base / 2
    center_y = base / 2
    center_z = base / 2

    # Ajustar a escala para que o cubo caiba na tela
    scale_factor = min(py5.width, py5.height) / (
        base * 40
    )  

    vinte = base * scale_factor
    py5.translate(py5.width / 2, py5.height / 2, 0)
    py5.scale(scale_factor)
    py5.translate(-center_x * vinte, -center_y * vinte, -200)

    py5.translate(center_x * vinte, center_y * vinte, center_z * vinte)
    # Desenhar a esfera no centro do cubo
    py5.rotate_x(py5.radians(rotate_x_angle))
    py5.rotate_y(py5.radians(rotate_y_angle))      
    
        
    py5.translate(-center_x * vinte, -center_y * vinte, -center_z * vinte)
    
    # Desenhar as faces do cubo
    if face is not None:
        py5.no_stroke()
        py5.fill(255, 0, 0, 50)  # Vermelho transparente
        draw_face(cantos_base[0], cantos_base[1], cantos_topo[1], cantos_topo[0])
        py5.fill(0, 255, 0, 50)  # Verde transparente
        draw_face(cantos_base[1], cantos_base[2], cantos_topo[2], cantos_topo[1])
        py5.fill(0, 0, 255, 50)  # Azul transparente
        draw_face(cantos_base[2], cantos_base[3], cantos_topo[3], cantos_topo[2])
        py5.fill(255, 255, 0, 50)  # Amarelo transparente
        draw_face(cantos_base[3], cantos_base[0], cantos_topo[0], cantos_topo[3])
        py5.fill(255, 0, 255, 50)  # Magenta transparente
        draw_face(cantos_topo[0], cantos_topo[1], cantos_topo[2], cantos_topo[3])
        py5.fill(0, 255, 255, 50)  # Ciano transparente
        draw_face(cantos_base[0], cantos_base[1], cantos_base[2], cantos_base[3])

    # Desenhar as arestas do cubo
    py5.stroke(0)
    py5.no_fill()
    for aresta in cube_edges:
        py5.line(
            aresta[0][0] * vinte,
            aresta[0][1] * vinte,
            aresta[0][2] * vinte,
            aresta[1][0] * vinte,
            aresta[1][1] * vinte,
            aresta[1][2] * vinte,
        )

    # Desenha matriz
    py5.stroke(0)
    py5.fill(0, 0, 255)
    for i in range(len(matriz) - 1):
        py5.line(
            matriz[i][0] * vinte,
            matriz[i][1] * vinte,
            matriz[i][2] * vinte,
            matriz[i + 1][0] * vinte,
            matriz[i + 1][1] * vinte,
            matriz[i + 1][2] * vinte,
        )
    
     # Adicionar marcadores visuais no primeiro e no último ponto da matriz
    if matriz:
        py5.no_stroke()
        py5.push_matrix()
        py5.fill(0, 255, 0)  # Verde para o primeiro ponto
        py5.translate(matriz[0][0] * vinte, matriz[0][1] * vinte, matriz[0][2] * vinte)
        py5.sphere(center_x)
        py5.pop_matrix()

        py5.push_matrix()
        py5.fill(255, 0, 0)  # Vermelho para o último ponto
        py5.translate(matriz[-1][0] * vinte, matriz[-1][1] * vinte, matriz[-1][2] * vinte)
        py5.sphere(center_x)
        py5.pop_matrix()

def draw_face(p1, p2, p3, p4):
    py5.begin_shape()
    py5.vertex(p1[0] * 20, p1[1] * 20, p1[2] * 20)
    py5.vertex(p2[0] * 20, p2[1] * 20, p2[2] * 20)
    py5.vertex(p3[0] * 20, p3[1] * 20, p3[2] * 20)
    py5.vertex(p4[0] * 20, p4[1] * 20, p4[2] * 20)
    py5.end_shape(py5.CLOSE)


def key_pressed():
    global rotate_x_angle, rotate_y_angle, rotate_speed, seed, frames_dir
    if py5.key == 'z' or py5.key == 'Z':
        create_gif(frames_dir, seed)
    elif py5.key == "w" or py5.key == 'W':
        rotate_x_angle -= rotate_speed
        print(rotate_x_angle, rotate_y_angle)
    elif py5.key == "s" or py5.key == 'S':
        rotate_x_angle += rotate_speed
        print(rotate_x_angle, rotate_y_angle)
    elif py5.key == "a" or py5.key == 'A':
        rotate_y_angle -= rotate_speed
        print(rotate_x_angle, rotate_y_angle)
    elif py5.key == "d" or py5.key == 'D':
        rotate_y_angle += rotate_speed
        print(rotate_x_angle, rotate_y_angle)
        
    py5.redraw()
    

def mouse_dragged():
    global rotate_x_angle, rotate_y_angle
    rotate_x_angle += py5.mouse_y - py5.pmouse_y
    rotate_y_angle += py5.mouse_x - py5.pmouse_x
    py5.redraw()

def key_pressed():
    global seed, frames_dir
    if py5.key == 'z' or py5.key == 'Z':
        create_gif(frames_dir, seed)

angle = 0
base = 10
size = 10
rotate_x_angle = 0
rotate_y_angle = 0
rotate_speed = 90
cubo = generate_cube(base, size)
matriz = generate_matrix(base, size)
face = None

frames_dir = save_frames(seed, limit=333, start=0)
py5.run_sketch(block=False)

while True:
    import time
    angle += 0.01
    rotate_x_angle += 5 * py5.sin(angle)
    rotate_y_angle += 5 * py5.cos(angle)
    time.sleep(0.1)
    py5.redraw()