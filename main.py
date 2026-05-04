"""Punto de entrada de consola para el Lab 07."""

from __future__ import annotations

import argparse

from duelo_ia_ia import run_duel_experiment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lab 07 - Tic-Tac-Toe")
    parser.add_argument("--duel", action="store_true", help="Ejecuta el duelo IA-IA del ejercicio 3.")
    parser.add_argument("--size", type=int, default=3, help="Tamaño del tablero para el duelo.")
    parser.add_argument("--games", type=int, default=20, help="Cantidad de partidas para el duelo.")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.duel:
        run_duel_experiment(size=args.size, games=args.games)
        return

    print("Usa --duel para ejecutar el ejercicio 3. Ejemplo: python main.py --duel")


if __name__ == "__main__":
    main()