import time
import threading
import numpy as np

class ECA:
    def __init__(self, steps=50):
        self.steps = steps
        self.evolution_history = None
        self.temp_evolution_history = None
        self.step = 0
        self.direction = 1

    def apply_rule(self, rule, state, x, y):
        """
        Aplica a regra de evolução celular para a célula na posição (x, y).
        """
        neighbors = [
            state[(x - 1) % state.shape[0], (y - 1) % state.shape[1]],  # cima-esquerda
            state[(x - 1) % state.shape[0], y],                         # cima
            state[(x - 1) % state.shape[0], (y + 1) % state.shape[1]],  # cima-direita
            state[x, (y - 1) % state.shape[1]],                         # esquerda
            state[x, (y + 1) % state.shape[1]],                         # direita
            state[(x + 1) % state.shape[0], (y - 1) % state.shape[1]],  # baixo-esquerda
            state[(x + 1) % state.shape[0], y],                         # baixo
            state[(x + 1) % state.shape[0], (y + 1) % state.shape[1]]   # baixo-direita
        ]
        index = sum([2**i * neighbors[i] for i in range(8)])
        return rule[index]

    def evolve(self, rule, initial_state, steps, temp=False):
        """
        Evolui o estado inicial das células por um número de passos, aplicando a regra especificada.
        """
        start_time = time.time()
        state = initial_state.copy()
        history = [state.copy()]

        for step in range(steps):
            new_state = np.zeros_like(state)
            for x in range(state.shape[0]):
                for y in range(state.shape[1]):
                    new_state[x, y] = self.apply_rule(rule, state, x, y)
            state = new_state
            history.append(state.copy())
            time.sleep(0.02)  # Adiciona um pequeno intervalo de descanso

        end_time = time.time()
        print(f"evolve function took {end_time - start_time:.4f} seconds")
        if temp:
            self.temp_evolution_history = history
        else:
            return history

    def plot_evolution(self):
        """
        Atualiza a evolução histórica temporária e reinicia o passo e a direção.
        """
        self.evolution_history = self.temp_evolution_history
        self.step = 0
        self.direction = 1

    def start(self, update=True):
        """
        Inicia a evolução das células, possivelmente em uma thread separada.
        """
        start_time = time.time()
        rule = np.random.randint(0, 2, size=256)  # Defina sua regra de 8 vizinhos aqui

        initial_state = np.zeros((self.steps, self.steps), dtype=int)
        initial_state[25, 25] = 1  # Estado inicial

        def generate_evolution():
            print("Evolution thread started")
            self.evolve(rule, initial_state, self.steps, temp=True)
            print("Evolution thread finished")

        if update:
            ev_history = self.evolve(rule, initial_state, self.steps)
            self.evolution_history = ev_history
            self.step = 0
            self.direction = 1
        else:
            threading.Thread(target=generate_evolution).start()

        end_time = time.time()
        print(f"start function took {end_time - start_time:.4f} seconds")