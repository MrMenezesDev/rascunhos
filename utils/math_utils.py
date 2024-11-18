
import math

def get_rotation_in_line(x1, y1, x2, y2, angle):

    # Vetor AB (de A para B)
    AB_x = x2 - x1
    AB_y = y2 - y1

    # Ângulo de rotação (30 graus convertidos para radianos)
    angulo_radianos = math.radians(angle)

    # Matriz de rotação
    cos_theta = math.cos(angulo_radianos)
    sin_theta = math.sin(angulo_radianos)

    # Vetor AC (rotacionado)
    AC_x = cos_theta * AB_x - sin_theta * AB_y
    AC_y = sin_theta * AB_x + cos_theta * AB_y

    # Coordenadas do ponto C
    x_C = x1 + AC_x
    y_C = y1 + AC_y

    return x_C, y_C

def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None  # Linhas são paralelas
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
    return px, py
