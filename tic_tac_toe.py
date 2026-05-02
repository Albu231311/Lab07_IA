import math
import time
import random


class TicTacToeEngine:
    
    #Clase que representa el "cerebro" y el estado del juego.
    #No contiene lógica de interfaz de usuario, solo procesamiento de datos.
    
    def __init__(self, size=3):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.nodes_explored = 0

    def is_empty(self, row, col):
        #Retorna si una celda está disponible.
        return self.board[row][col] == ' '

    def get_moves(self):
        #Retorna lista de coordenadas (r, c) disponibles.
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == ' ']

    def is_winner(self, player):
        #Verifica si el jugador ha ganado."""
        for i in range(self.size):
            if all([self.board[i][j] == player for j in range(self.size)]): return True
            if all([self.board[j][i] == player for j in range(self.size)]): return True
        if all([self.board[i][i] == player for i in range(self.size)]): return True
        if all([self.board[i][self.size - 1 - i] == player for i in range(self.size)]): return True
        return False

    def is_terminal(self):
        #Verifica si el juego terminó (victoria o empate)."""
        return self.is_winner('X') or self.is_winner('O') or len(self.get_moves()) == 0

    def evaluate(self):
        
        #Función heurística para tableros no terminados.
        #Evalúa todas las filas, columnas y diagonales para asignar
        #un puntaje basado en la proximidad a ganar de cada jugador.
        
        if self.is_winner('X'): return 100000
        if self.is_winner('O'): return -100000
        if len(self.get_moves()) == 0: return 0

        score = 0
        lines = []
        for i in range(self.size):
            lines.append(self.board[i])
            lines.append([self.board[j][i] for j in range(self.size)])
        lines.append([self.board[i][i] for i in range(self.size)])
        lines.append([self.board[i][self.size - 1 - i] for i in range(self.size)])

        for line in lines:
            score += self._evaluate_line(line)
        return score

    def _evaluate_line(self, line):
        #Asigna un valor a una línea dependiendo de las fichas que contiene
        x_count = line.count('X')
        o_count = line.count('O')
        if x_count > 0 and o_count > 0:
            return 0
        if x_count > 0:
            return 10 ** x_count
        elif o_count > 0:
            return -(10 ** o_count)
        return 0

    def minimax_pure(self, is_maximizing, player='X'):
        #Implementación exhaustiva (solo recomendada para 3x3)
        self.nodes_explored += 1
        opponent = 'O' if player == 'X' else 'X'

        if self.is_winner(player): return 100000 if is_maximizing else -100000
        if self.is_winner(opponent): return -100000 if is_maximizing else 100000
        if len(self.get_moves()) == 0: return 0

        if is_maximizing:
            best_score = -math.inf
            for r, c in self.get_moves():
                self.board[r][c] = player
                score = self.minimax_pure(False, player)
                self.board[r][c] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for r, c in self.get_moves():
                self.board[r][c] = opponent
                score = self.minimax_pure(True, player)
                self.board[r][c] = ' '
                best_score = min(score, best_score)
            return best_score

    def minimax_limit(self, depth, is_maximizing, player='X'):
        #Minimax que se detiene en un horizonte fijo y usa evaluate().
        self.nodes_explored += 1
        opponent = 'O' if player == 'X' else 'X'

        if depth == 0 or self.is_terminal():
            return self.evaluate()

        if is_maximizing:
            best_score = -math.inf
            for r, c in self.get_moves():
                self.board[r][c] = player
                score = self.minimax_limit(depth - 1, False, player)
                self.board[r][c] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for r, c in self.get_moves():
                self.board[r][c] = opponent
                score = self.minimax_limit(depth - 1, True, player)
                self.board[r][c] = ' '
                best_score = min(score, best_score)
            return best_score

    def alpha_beta(self, depth, alpha, beta, is_maximizing, player='X'):
        #Minimax optimizado con poda alfa-beta
        self.nodes_explored += 1
        opponent = 'O' if player == 'X' else 'X'

        if depth == 0 or self.is_terminal():
            return self.evaluate()

        if is_maximizing:
            best_score = -math.inf
            for r, c in self.get_moves():
                self.board[r][c] = player
                score = self.alpha_beta(depth - 1, alpha, beta, False, player)
                self.board[r][c] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = math.inf
            for r, c in self.get_moves():
                self.board[r][c] = opponent
                score = self.alpha_beta(depth - 1, alpha, beta, True, player)
                self.board[r][c] = ' '
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

    def mcts(self, iterations, C, player='X'):
        
        #Monte Carlo Tree Search utilizando la fórmula UCT para selección.
        #UCT = mean_win_rate + C * sqrt(ln(ParentVisits) / NodeVisits)
        #Retorna la mejor jugada (r, c).
        
        opponent = 'O' if player == 'X' else 'X'

        class MCTSNode:
            def __init__(self, move=None, parent=None, player_who_moved=None):
                self.move = move
                self.parent = parent
                self.player_who_moved = player_who_moved
                self.wins = 0.0
                self.visits = 0
                self.children = []
                self.untried_moves = None

        def board_copy():
            return [row[:] for row in self.board]

        def get_moves_from(board):
            return [(r, c) for r in range(self.size) for c in range(self.size) if board[r][c] == ' ']

        def check_winner(board, p):
            sz = self.size
            for i in range(sz):
                if all(board[i][j] == p for j in range(sz)): return True
                if all(board[j][i] == p for j in range(sz)): return True
            if all(board[i][i] == p for i in range(sz)): return True
            if all(board[i][sz - 1 - i] == p for i in range(sz)): return True
            return False

        def is_terminal_board(board):
            return check_winner(board, 'X') or check_winner(board, 'O') or len(get_moves_from(board)) == 0

        def uct_score(node, parent_visits):
            if node.visits == 0:
                return math.inf
            return (node.wins / node.visits) + C * math.sqrt(math.log(parent_visits) / node.visits)

        def select(node, board, current_player):
            #Baja por el árbol eligiendo hijos con mayor UCT hasta llegar a uno no expandido o terminal.
            while not is_terminal_board(board):
                if node.untried_moves is None:
                    node.untried_moves = get_moves_from(board)[:]
                if node.untried_moves:
                    return expand(node, board, current_player)
                next_player = 'O' if current_player == 'X' else 'X'
                node = max(node.children, key=lambda c: uct_score(c, node.visits))
                r, c = node.move
                board[r][c] = current_player
                current_player = next_player
            return node, board, current_player

        def expand(node, board, current_player):
            #Expande un movimiento no probado del nodo.
            move = random.choice(node.untried_moves)
            node.untried_moves.remove(move)
            r, c = move
            board[r][c] = current_player
            next_player = 'O' if current_player == 'X' else 'X'
            child = MCTSNode(move=move, parent=node, player_who_moved=current_player)
            child.untried_moves = get_moves_from(board)[:]
            node.children.append(child)
            return child, board, next_player

        def simulate(board, current_player):
            #Simulación aleatoria (rollout) hasta el final del juego.
            board = [row[:] for row in board]
            p = current_player
            while not is_terminal_board(board):
                moves = get_moves_from(board)
                r, c = random.choice(moves)
                board[r][c] = p
                p = 'O' if p == 'X' else 'X'
            if check_winner(board, player): return 1.0
            elif check_winner(board, opponent): return 0.0
            else: return 0.5

        def backpropagate(node, result):
            #Propaga el resultado hacia la raíz
            while node is not None:
                node.visits += 1
                if node.player_who_moved == player:
                    node.wins += result
                else:
                    node.wins += (1.0 - result)
                node = node.parent

        root = MCTSNode(player_who_moved=None)
        root.untried_moves = get_moves_from(self.board)[:]

        for _ in range(iterations):
            self.nodes_explored += 1
            sim_board = board_copy()
            current_player = player
            node, sim_board, current_player = select(root, sim_board, current_player)
            result = simulate(sim_board, current_player)
            backpropagate(node, result)

        if not root.children:
            moves = self.get_moves()
            return random.choice(moves) if moves else None

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move

    def get_best_move(self, algo, depth=None, player='X', N=500, C=math.sqrt(2)):
        #Lanza el algoritmo seleccionado y devuelve la mejor jugada.
        self.nodes_explored = 0

        if algo == 'mcts':
            return self.mcts(N, C, player)

        best_score = -math.inf
        best_move = None

        for r, c in self.get_moves():
            self.board[r][c] = player

            if algo == 'alpha_beta':
                score = self.alpha_beta(depth - 1, -math.inf, math.inf, False, player)
            elif algo == 'minimax_limit':
                score = self.minimax_limit(depth - 1, False, player)
            elif algo == 'minimax_pure':
                score = self.minimax_pure(False, player)
            else:
                score = 0

            self.board[r][c] = ' '
            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move
    

class GameLoop:
    
    #Clase que orquesta el flujo de la partida.
    
    def __init__(self, size=3, mode="H-IA", starting_player="H", ia_configs=None):
        self.engine = TicTacToeEngine(size)
        self.mode = mode
        self.current_player = 'X'

        if ia_configs is None:
            self.ia_configs = {
                'IA1': {'algo': 'alpha_beta', 'depth': 4, 'N': 500, 'C': math.sqrt(2)},
                'IA2': {'algo': 'mcts',        'depth': 4, 'N': 500, 'C': math.sqrt(2)}
            }
        else:
            self.ia_configs = ia_configs

        if mode == "H-IA":
            self.roles = {'X': 'Humano', 'O': 'IA1'} if starting_player == 'H' else {'X': 'IA1', 'O': 'Humano'}
        elif mode == "IA-IA":
            self.roles = {'X': 'IA1', 'O': 'IA2'}
        else:
            self.roles = {'X': 'Humano 1', 'O': 'Humano 2'}

    def print_board(self):
        #Imprime el tablero tras cada movimiento
        for row in self.engine.board:
            print(" | ".join(row))
            print("-" * (self.engine.size * 4 - 1))

    def play(self):
        print(f"Iniciando partida {self.engine.size}x{self.engine.size} | Modo: {self.mode}")
        self.print_board()

        while not self.engine.is_terminal():
            role = self.roles[self.current_player]
            print(f"\nTurno de {role} ({self.current_player})")

            start_time = time.time()
            nodes = 0

            if "Humano" in role:
                valid_move = False
                while not valid_move:
                    try:
                        move = input("Ingresa fila y columna separadas por espacio (ej. '0 1'): ")
                        r, c = map(int, move.split())
                        if 0 <= r < self.engine.size and 0 <= c < self.engine.size and self.engine.is_empty(r, c):
                            self.engine.board[r][c] = self.current_player
                            valid_move = True
                        else:
                            print("Casilla ocupada o fuera de rango. Intenta de nuevo.")
                    except (ValueError, IndexError):
                        print("Entrada inválida. Asegúrate de ingresar coordenadas dentro del tablero.")
            else:
                config = self.ia_configs[role]
                algo  = config['algo']
                depth = config.get('depth', 4)
                N     = config.get('N', 500)
                C     = config.get('C', math.sqrt(2))

                move = self.engine.get_best_move(algo, depth, self.current_player, N, C)

                if move:
                    self.engine.board[move[0]][move[1]] = self.current_player
                nodes = self.engine.nodes_explored

            elapsed_time = time.time() - start_time

            self.print_board()
            if "IA" in role:
                print(f"[{role}] Nodos explorados: {nodes} | Tiempo: {elapsed_time:.4f}s")

            self.current_player = 'O' if self.current_player == 'X' else 'X'

        if self.engine.is_winner('X'):
            print(f"\n¡Ha ganado {self.roles['X']} (X)!")
        elif self.engine.is_winner('O'):
            print(f"\n¡Ha ganado {self.roles['O']} (O)!")
        else:
            print("\n¡Es un empate!")


#Bloque de ejecución para pruebas rápidas. Se puede modificar para probar diferentes configuraciones o modos.
if __name__ == "__main__":
    configs = {
        'IA1': {'algo': 'alpha_beta', 'depth': 4, 'N': 500, 'C': math.sqrt(2)}
    }
    game = GameLoop(size=3, mode="H-IA", starting_player="IA", ia_configs=configs)
    game.play()
