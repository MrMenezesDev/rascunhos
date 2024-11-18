from dataclasses import dataclass, field
from functools import cached_property
from itertools import product
import random

@dataclass
class Tile:
    """
    Esta classe representa uma imagem de tile do py5 com suas bordas de possíveis conexões.
    A lista de bordas (edges) representa os tipos possíveis de conexão entre este tile e seus vizinhos.
    A posição da conexão na lista de bordas indica a orientação delas.
    """
    edges: list
    
    def get_side(self, side):
        return self.edges[side]

@dataclass
class Cell:
    col: int
    row: int
    dim: tuple[int, int]
    border: bool = False
    tile: Tile = field(default=None, init=False)  
    state: list = field(default_factory=lambda: [None, None, None, None, None, None])
    cases: list = field(default_factory=lambda: [0, 1])
            
    def __post_init__(self):
        if self.border:
            self.update_border_state()
            

    @property
    def collapsed(self):
        return self.tile is not None

    def collapse(self):
        edges = []
        for state in self.state:
            if state is not None:
                edges.append(state)
            else:
                edges.append(random.choice(self.cases))
        self.tile = Tile(edges)    

    @property
    def entropy(self):
        if self.collapsed:
            return 0
        return len([state for state in self.state if state is not None]) ** len(self.cases)

    def update_border_state(self):
        if self.col == 0:
            self.state[4] = 0
            self.state[5] = 0
        if self.col == self.dim[0] - 1:
            self.state[1] = 0
            self.state[2] = 0
        if self.row == 0:
            self.state[0] = 0
            if self.col % 2 == 0:
                self.state[1] = 0
                self.state[5] = 0
        if self.row == self.dim[1] - 1:
            self.state[3] = 0
            if self.col % 2 != 0:
                self.state[2] = 0
                self.state[4] = 0        
             

    def update_state(self, neighbor_number, value):
        index = [3,4,5,0,1,2][neighbor_number]
        self.state[index] = value


@dataclass
class HexWaveFunctionCollapseGrid:
    """
    Classe WaveFunctionCollapseGrid
    ===============================
    Classe para representar uma grade que será populada colapsando suas células.
    Atributos:
    ----------
    tiles : list
        Lista de tiles disponíveis para a grade.
    dim : int
        Dimensão da grade.
    pending_cells : list[Cell]
        Lista de células pendentes que ainda não foram colapsadas.
    Métodos:
    --------
    __post_init__():
        Inicializa a lista de células pendentes com uma cópia das células e embaralha a lista.
    w():
        Retorna a largura de cada célula na grade.
    h():
        Retorna a altura de cada célula na grade.
    cells():
        Retorna uma lista de células inicializadas com todas as tiles possíveis.
    start():
        Inicia o algoritmo escolhendo uma célula aleatória e colapsando-a.
    collapse_cell(cell):
        Colapsa a célula especificada, remove-a da lista de células pendentes e atualiza as opções das células vizinhas.
    get_neighbors(cell):
        Dada uma célula, retorna a lista de vizinhos que ainda não foram colapsados.
    complete():
        Retorna True se todas as células foram colapsadas, caso contrário, False.
    collapse():
        Obtém a próxima célula pendente com a menor entropia e a colapsa.
    draw():
        Desenha a grade, exibindo as imagens das células colapsadas.
    Class to represent a grid which will be populated by collapsing their cells.
    """

    dim: tuple[int, int]
    pending_cells: list[Cell] = field(default=list, init=False)
    draw_cell: callable
    border: bool = False
    
    def __post_init__(self):        
        self.pending_cells = self.cells[:] 
        random.shuffle(self.pending_cells)

    @cached_property
    def cells(self):
        return [
            Cell(col=i, row=j, dim=self.dim, border=self.border) 
            for i, j in product(range(0, self.dim[0]), range(0, self.dim[1]))
        ]

    def start(self):
        """
        To start the algorithm, we pick any random cell and collapse it since all of them have the
        same set of possible tiles.
        """
        cell = random.choice(self.cells)
        self.collapse_cell(cell)

    def collapse_cell(self, cell: Cell):
        cell.collapse()
        self.pending_cells.remove(cell)
        for index, neighbor_cell in self.get_neighbors(cell):
            neighbor_cell.update_state(neighbor_number=index, value=cell.tile.get_side(index))

    def get_neighbors(self, cell: Cell):
        """
        Given a cell, return its list of neighbors which still weren't collapsed.
        """
        i, j = cell.col, cell.row
        positions = [
            (i, j - 1),
            (i + 1, j - 1) if i % 2 == 0 else(i + 1, j) ,
            (i + 1, j) if i % 2 == 0 else (i + 1, j + 1),
            (i, j + 1),
            (i - 1, j) if i % 2 == 0 else (i - 1, j + 1),
            (i - 1, j - 1) if i % 2 == 0 else (i - 1, j),
        ]

        #       1,0  
        # 0,1 - 1,1 - 2,1
        # 0,2 - 1,2 - 2,2
        
        #        2,1
        #  1,1 - 2,2 - 3,1
        #  1,2 - 2,3 - 3,2
        
        neighbors = [
            (index, c) for index, pos in enumerate(positions)
            for c in self.pending_cells if (c.col, c.row) == pos
        ]
        return neighbors

    @property
    def complete(self):
        return not self.pending_cells

    def collapse(self):
        if not self.pending_cells:
            return  # Se não houver células pendentes, retorne imediatamente

        next_cell = sorted(self.pending_cells, key=lambda c: c.entropy)[0]
        # Resto do código da função collapse
        self.collapse_cell(next_cell)

    def draw(self):
        for cell in self.cells:
            if cell.collapsed:
                self.draw_cell(cell)