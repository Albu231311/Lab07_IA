"""Experimento de duelo IA-IA para Tic-Tac-Toe.

IA-1 usa MCTS con N=500 y C=sqrt(2).
IA-2 usa Minimax limitado a depth=4 con poda Alpha-Beta.
"""

from __future__ import annotations

import argparse
import math
import time
from dataclasses import dataclass

from tic_tac_toe import TicTacToeEngine


@dataclass
class GameResult:
    game_number: int
    starting_ai: str
    winner: str
    moves: int
    ai1_moves: int
    ai2_moves: int
    ai1_time: float
    ai2_time: float
    ai1_avg_time: float
    ai2_avg_time: float
    ai1_nodes: int
    ai2_nodes: int


def _ai_configs() -> dict[str, dict[str, float | int | str]]:
    return {
        "IA-1": {"algo": "mcts", "N": 500, "C": math.sqrt(2)},
        "IA-2": {"algo": "alpha_beta", "depth": 4},
    }


def _opponent(ai_name: str) -> str:
    return "IA-2" if ai_name == "IA-1" else "IA-1"


def _winner_from_board(engine: TicTacToeEngine, symbol_to_ai: dict[str, str]) -> str:
    if engine.is_winner("X"):
        return symbol_to_ai["X"]
    if engine.is_winner("O"):
        return symbol_to_ai["O"]
    return "Empate"


def _format_time(value: float) -> str:
    return f"{value:.4f} s"


def _play_single_game(game_number: int, size: int) -> GameResult:
    engine = TicTacToeEngine(size=size)
    configs = _ai_configs()
    starting_ai = "IA-1" if game_number % 2 == 1 else "IA-2"
    symbol_to_ai = {"X": starting_ai, "O": _opponent(starting_ai)}

    ai_time = {"IA-1": 0.0, "IA-2": 0.0}
    ai_moves = {"IA-1": 0, "IA-2": 0}
    ai_nodes = {"IA-1": 0, "IA-2": 0}
    current_symbol = "X"

    while not engine.is_terminal():
        ai_name = symbol_to_ai[current_symbol]
        config = configs[ai_name]

        start = time.perf_counter()
        move = engine.get_best_move(
            config["algo"],
            depth=int(config.get("depth", 4)),
            player=current_symbol,
            N=int(config.get("N", 500)),
            C=float(config.get("C", math.sqrt(2))),
        )
        elapsed = time.perf_counter() - start

        if move is None:
            raise RuntimeError(
                f"No se pudo calcular un movimiento valido en la partida {game_number}."
            )

        engine.board[move[0]][move[1]] = current_symbol
        ai_time[ai_name] += elapsed
        ai_moves[ai_name] += 1
        ai_nodes[ai_name] += engine.nodes_explored
        current_symbol = "O" if current_symbol == "X" else "X"

    winner = _winner_from_board(engine, symbol_to_ai)

    ai1_avg = ai_time["IA-1"] / ai_moves["IA-1"] if ai_moves["IA-1"] else 0.0
    ai2_avg = ai_time["IA-2"] / ai_moves["IA-2"] if ai_moves["IA-2"] else 0.0

    return GameResult(
        game_number=game_number,
        starting_ai=starting_ai,
        winner=winner,
        moves=sum(ai_moves.values()),
        ai1_moves=ai_moves["IA-1"],
        ai2_moves=ai_moves["IA-2"],
        ai1_time=ai_time["IA-1"],
        ai2_time=ai_time["IA-2"],
        ai1_avg_time=ai1_avg,
        ai2_avg_time=ai2_avg,
        ai1_nodes=ai_nodes["IA-1"],
        ai2_nodes=ai_nodes["IA-2"],
    )


def _print_game_result(result: GameResult) -> None:
    print(f"Partida {result.game_number:02d}")
    print(f"  Inicia: {result.starting_ai}")
    print(f"  Ganador: {result.winner}")
    print(f"  Movimientos realizados: {result.moves}")
    print(
        f"  IA-1 -> movimientos: {result.ai1_moves} | tiempo total: {_format_time(result.ai1_time)} | "
        f"promedio: {_format_time(result.ai1_avg_time)} | nodos/iteraciones: {result.ai1_nodes}"
    )
    print(
        f"  IA-2 -> movimientos: {result.ai2_moves} | tiempo total: {_format_time(result.ai2_time)} | "
        f"promedio: {_format_time(result.ai2_avg_time)} | nodos/iteraciones: {result.ai2_nodes}"
    )
    print()


def run_duel_experiment(size: int = 3, games: int = 20) -> list[GameResult]:
    if size < 3:
        raise ValueError("El tablero debe ser de al menos 3x3.")
    if games <= 0:
        raise ValueError("La cantidad de partidas debe ser mayor que cero.")

    print("===== DUELO IA-IA =====")
    print(f"Tablero: {size}x{size}")
    print(f"Partidas programadas: {games}")
    print()

    results: list[GameResult] = []
    for game_number in range(1, games + 1):
        result = _play_single_game(game_number, size)
        results.append(result)
        _print_game_result(result)

    ai1_wins = sum(1 for result in results if result.winner == "IA-1")
    ai2_wins = sum(1 for result in results if result.winner == "IA-2")
    draws = sum(1 for result in results if result.winner == "Empate")
    ai1_time_total = sum(result.ai1_time for result in results)
    ai2_time_total = sum(result.ai2_time for result in results)
    ai1_moves_total = sum(result.ai1_moves for result in results)
    ai2_moves_total = sum(result.ai2_moves for result in results)
    ai1_avg = ai1_time_total / ai1_moves_total if ai1_moves_total else 0.0
    ai2_avg = ai2_time_total / ai2_moves_total if ai2_moves_total else 0.0

    ai1_win_pct = (ai1_wins / games) * 100 if games else 0.0
    ai2_win_pct = (ai2_wins / games) * 100 if games else 0.0

    print("===== RESUMEN DUELO IA-IA =====")
    print(f"Partidas jugadas: {games}")
    print()
    print("IA-1: MCTS, N=500, C=sqrt(2)")
    print("IA-2: Minimax depth=4 + Alpha-Beta")
    print()
    print(f"Victorias IA-1: {ai1_wins}")
    print(f"Victorias IA-2: {ai2_wins}")
    print(f"Empates: {draws}")
    print()
    print(f"Porcentaje victoria IA-1: {ai1_win_pct:.2f}%")
    print(f"Porcentaje victoria IA-2: {ai2_win_pct:.2f}%")
    print(f"Tiempo promedio por jugada IA-1: {_format_time(ai1_avg)}")
    print(f"Tiempo promedio por jugada IA-2: {_format_time(ai2_avg)}")
    print()

    if ai1_wins > ai2_wins:
        smarter_text = "IA más inteligente según victorias: IA-1"
        smart_conclusion = "IA-1 fue la que ganó más partidas."
    elif ai2_wins > ai1_wins:
        smarter_text = "IA más inteligente según victorias: IA-2"
        smart_conclusion = "IA-2 fue la que ganó más partidas."
    else:
        smarter_text = "IA más inteligente según victorias: No hubo una IA claramente más inteligente"
        smart_conclusion = "Ambas IA terminaron con el mismo número de victorias."

    time_gap = abs(ai1_avg - ai2_avg)
    if time_gap <= 0.001 or (max(ai1_avg, ai2_avg) > 0 and time_gap / max(ai1_avg, ai2_avg) <= 0.05):
        efficient_text = "IA más eficiente según tiempo por jugada: diferencia mínima entre ambas"
        time_conclusion = "La diferencia de tiempo promedio por jugada fue muy pequeña."
    elif ai1_avg < ai2_avg:
        efficient_text = "IA más eficiente según tiempo por jugada: IA-1"
        time_conclusion = "IA-1 consumió menos tiempo promedio por jugada."
    else:
        efficient_text = "IA más eficiente según tiempo por jugada: IA-2"
        time_conclusion = "IA-2 consumió menos tiempo promedio por jugada."

    print(smarter_text)
    print(efficient_text)
    print()
    print("Conclusión:")
    print(f"Después de {games} partidas, {smart_conclusion} {time_conclusion}")

    return results


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ejercicio 3 - Duelo IA-IA en Tic-Tac-Toe")
    parser.add_argument("--size", type=int, default=3, help="Tamaño del tablero, por ejemplo 3 o 4.")
    parser.add_argument("--games", type=int, default=20, help="Cantidad de partidas a ejecutar.")
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    run_duel_experiment(size=args.size, games=args.games)


if __name__ == "__main__":
    main()