from typing import Callable, List


class Zentangle:
    height: int
    width: int
    border_size: int = 2
    background_color: str = "#FFFFFF"
    spacing: int = 8
    border_color: str = "#000000"
    rule: Callable = None

    def __init__(self, height: int, width: int, rule=None, spacing: int = 8):
        self.height = height
        self.width = width
        self.rule = rule
        self.spacing = spacing

    def animate(self, **kargs):
        self.rule(self, "animate", kargs)

    def draw(self, **kargs):
        self.rule(self, "draw", kargs)


class Layout:
    zentalgles: List[Zentangle] = []
    height: int
    width: int

    def __init__(self, height: int, width: int, zentalgles: List[Zentangle] = []):
        self.height = height
        self.width = width
        self.zentalgles = zentalgles

    def __post_init__(self):
        if len(self.zentalgles) > 0:
            self.__validate__(self.zentalgles[0])

    def add_zentangle(self, zen: Zentangle | List[Zentangle]):
        if zen is list:
            self.__validate__(zen[0], len(zen))
            self.zentalgles += zen
        else:
            self.__validate__(zen)
            self.zentalgles.append(zen)

    def __validate__(self, zen: Zentangle, n: int = 1):
        lines = int(self.height / (zen.height + zen.spacing))
        cols = int(self.width / (zen.width + zen.spacing))

        if cols * lines < len(self.zentalgles) + n:
            raise ValueError(
                "The number of zentangles must be equal to the number of rows times the number of columns"
            )

    def draw(self):
        for zen in self.zentalgles:
            zen.draw()

    def animate_grid(self):
        gen = self.zen_generator()
        try:
            zen = next(gen)
        except StopIteration:
            return

        lines = int(self.height / (zen.height + zen.spacing))
        cols = int(self.width / (zen.width + zen.spacing))

        for line in range(lines):
            for col in range(cols):
                zen.animate(col=col, line=line)
                try:
                    zen = next(gen)
                except StopIteration:
                    return

    def zen_generator(self):
        for zen in self.zentalgles:
            yield zen

    def draw_grid(self):
        gen = self.zen_generator()
        try:
            zen = next(gen)
        except StopIteration:
            return

        lines = int(self.height / (zen.height + zen.spacing))
        cols = int(self.width / (zen.width + zen.spacing))

        for line in range(lines):
            for col in range(cols):
                zen.draw(col=col, line=line)
                try:
                    zen = next(gen)
                except StopIteration:
                    return
