import numpy as np
import random, copy

def common_plans(p1, p2):
    cont = 0
    position = []
    for it in range(0, 3):
        if p1[it] == p2[it]:
            cont += 1
            position.append(it)
    return cont, position


def create_lines(p1, p2, ini):
    points = []
    temp1 = copy.copy(p1)
    temp2 = copy.copy(p2)
    c_plans, position = common_plans(p1, p2)
    axis = [0, 1, 2]
    if c_plans < 3:
        [i for i in position if not i in axis or axis.remove(i)]
        options = axis
        if c_plans > 1:
            rand = 0
        else:
            rand = random.randint(0, 2 - c_plans)
        p1[options[rand]] = p2[options[rand]]
        temp = create_lines(p1, p2, ini)
        if p1 != temp[len(temp) - 1] and len(temp) < 1:
            points.append(temp[1])
        elif p1 != temp[len(temp) - 1]:
            points = temp
        points.append(temp1)
        if ini == temp1:
            points.reverse()
            points.append(temp2)
        return points
    elif c_plans == 3:
        points.append(p1)
        return points


    xs = np.random.randint(0, base, size)
    ys = np.random.randint(0, base, size)
    zs = np.random.randint(0, base, size)
    
    xs1, ys1, zs1 = [], [], []
    mat3d = []
    
    for i in range(xs.size - 1):
        insert = create_lines([xs[i], ys[i], zs[i]], [xs[i+1], ys[i+1], zs[i+1]], [xs[i], ys[i], zs[i]])
        for coord in insert:
            xs1.append(coord[0])
            ys1.append(coord[1])
            zs1.append(coord[2])
    
    for i in range(len(xs1) - 1):
        mat3d.append([xs1[i], ys1[i], zs1[i]])
    return mat3d

def generate_random3_d_grid(base: int, size: int) -> list:
    """
    Gera uma grade 3D aleatória com base e tamanho especificados.
    Esta função cria três arrays de inteiros aleatórios (xs, ys, zs) dentro do intervalo [0, base].
    Em seguida, modifica o último elemento de um desses arrays com base em uma escolha aleatória.
    O primeiro elemento do array xs é definido como 0.
    A função então gera uma matriz 3D criando linhas entre pontos consecutivos nos arrays.
    Args:
        base (int): O limite superior para os inteiros aleatórios.
        size (int): O número de pontos em cada dimensão.
    Returns:
        list: Uma lista de coordenadas 3D representando a grade gerada.
    """
    xs = np.random.random_integers(0, base, size)
    ys = np.random.random_integers(0, base, size)
    zs = np.random.random_integers(0, base, size)

    rand = np.random.random_integers(1, 3, 1)

    if rand == 1:
        xs[size-1] = 0
    elif rand == 2:
        zs[size-1] = 0
    else:
        ys[size-1] = 0

    xs[0] = 0

    xs1, ys1, zs1 = [[], [], []]
    mat3d = []
    for i in range(0, xs.size-1):
        insert = create_lines([xs[i], ys[i], zs[i]], [xs[i+1], ys[i+1], zs[i+1]], [xs[i], ys[i], zs[i]])
        for coord in insert:
            xs1.append(coord[0])
            ys1.append(coord[1])
            zs1.append(coord[2])

    for i in range(0, len(xs1) - 1):
        mat3d.append([xs1[i], ys1[i], zs1[i]])
    
    return mat3d

def generate_cube_geometry(base):
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
