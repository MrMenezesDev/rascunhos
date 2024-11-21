import math
from typing import Callable
from spiral.spiral import Poligono
from zen.zentangle import Zentangle

def draw_spiral_poligono(sides:int, col, row, zen: Zentangle, initial_spacing, line: Callable,factor=0.1):
    points = []
    border_color, border_size, width, spacing, height = (
        zen.border_color,
        zen.border_size,
        zen.width,
        zen.spacing,
        zen.height,
    )
    
    x = (col * (width + spacing)) + initial_spacing
    y = (row * (height + spacing)) + initial_spacing
    
    # Marca os pontos do polígono
    for side in range(sides):
        points.append([x + width / 2 + width / 2 * math.cos(side * 2 * math.pi / sides), y + height / 2 + height / 2 * math.sin(side * 2 * math.pi / sides)])
    
    poli = Poligono(points)
    poli.display(line)
    poli.spiral(line, deep=50, factor=factor)