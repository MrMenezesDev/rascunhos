from typing import Callable

from utils.math_utils import dist_move


class Poligono:
    points = list()

    def __init__(self, points):
        self.points = points

    def display(self, line):
        for i in range(len(self.points)):
            if i + 1 > len(self.points) - 1:
                line(
                    self.points[i][0],
                    self.points[i][1],
                    self.points[0][0],
                    self.points[0][1],
                )
            else:
                line(
                    self.points[i][0],
                    self.points[i][1],
                    self.points[i + 1][0],
                    self.points[i + 1][1],
                )

    def spiral(self, line: Callable, deep=5, factor=0.1):
        temp = list()
        for i, point in enumerate(self.points):
            atual = point
            proximo = self.points[i + 1] if i + 1 < len(self.points) else self.points[0]
            dist = dist_move(atual, proximo, factor)
            temp.append(dist)

        poli = Poligono(temp)
        poli.display(line)
        if deep > 0:
            poli.spiral(line, deep - 1, factor)
        return poli