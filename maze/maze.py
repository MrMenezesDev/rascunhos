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

def generate_matrix(base, size):
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
    mat3d =[]
    for i in range(0, xs.size-1):
        insert = create_lines([xs[i], ys[i], zs[i]], [xs[i+1], ys[i+1], zs[i+1]], [xs[i], ys[i], zs[i]])
        for coord in insert:
            xs1.append(coord[0])
            ys1.append(coord[1])
            zs1.append(coord[2])

    for i in range(0, len(xs1) - 1):
        mat3d.append([xs1[i], ys1[i], zs1[i]])
    
    return mat3d

