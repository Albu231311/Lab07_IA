import math
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from tic_tac_toe import TicTacToeEngine


def bench_minimax(size, depths, player='X'):
    #Ejecuta minimax_limit desde tablero vacío para cada profundidad dada.
    #Retorna lista de tuplas (depth, nodos, tiempo_s).
    results = []
    for d in depths:
        engine = TicTacToeEngine(size)
        engine.nodes_explored = 0
        t0 = time.perf_counter()
        engine.minimax_limit(d, True, player)
        elapsed = time.perf_counter() - t0
        results.append((d, engine.nodes_explored, elapsed))
    return results


def bench_alpha_beta(size, depths, player='X'):
    #Ejecuta alpha_beta desde tablero vacío para cada profundidad dada.
    #Retorna lista de tuplas (depth, nodos, tiempo_s, ebf).
    results = []
    for d in depths:
        engine = TicTacToeEngine(size)
        engine.nodes_explored = 0
        t0 = time.perf_counter()
        engine.alpha_beta(d, -math.inf, math.inf, True, player)
        elapsed = time.perf_counter() - t0
        nodes = engine.nodes_explored
        ebf = nodes ** (1 / d) if d > 0 and nodes > 0 else 0
        results.append((d, nodes, elapsed, ebf))
    return results


def seccion_a1():
    #(a1) Búsqueda minimax en 3x3, depth 1-9.
    #Registra nodos visitados y tiempo de ejecución.
    print("(a1) Minimax 3x3 — depth 1 a 9")
    resultados = bench_minimax(size=3, depths=range(1, 10))

    print(f"{'Depth':>6} {'Nodos':>12} {'Tiempo (s)':>12}")
    for d, n, t in resultados:
        print(f"{d:>6} {n:>12,} {t:>12.6f}")

    depths = [r[0] for r in resultados]
    nodes  = [r[1] for r in resultados]
    times  = [r[2] for r in resultados]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('(a1) Minimax — Tic-Tac-Toe 3×3', fontsize=13, fontweight='bold')

    ax1.semilogy(depths, nodes, 'o-', color='#7F77DD', linewidth=2, markersize=6)
    ax1.set_title('Nodos explorados')
    ax1.set_xlabel('Profundidad')
    ax1.set_ylabel('Nodos (escala log)')
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax1.set_xticks(depths)
    ax1.grid(True, which='both', linestyle='--', alpha=0.4)

    ax2.plot(depths, times, 'o-', color='#7F77DD', linewidth=2, markersize=6)
    ax2.set_title('Tiempo de ejecución')
    ax2.set_xlabel('Profundidad')
    ax2.set_ylabel('Tiempo (s)')
    ax2.set_xticks(depths)
    ax2.grid(True, linestyle='--', alpha=0.4)

    plt.tight_layout()
    plt.savefig('a1_minimax.png', dpi=150, bbox_inches='tight')
    print("  Guardada: a1_minimax.png\n")
    plt.show()


def seccion_a2():
    #(a2) Búsqueda alpha-beta en 3x3, depth 1-9.
    #Registra nodos visitados y tiempo de ejecución.
    print("(a2) Alpha-β 3x3 — depth 1 a 9")
    resultados = bench_alpha_beta(size=3, depths=range(1, 10))

    print(f"{'Depth':>6} {'Nodos':>12} {'Tiempo (s)':>12}")
    for d, n, t, _ in resultados:
        print(f"{d:>6} {n:>12,} {t:>12.6f}")

    depths = [r[0] for r in resultados]
    nodes  = [r[1] for r in resultados]
    times  = [r[2] for r in resultados]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('(a2) Alpha-β — Tic-Tac-Toe 3×3', fontsize=13, fontweight='bold')

    ax1.semilogy(depths, nodes, 's--', color='#1D9E75', linewidth=2, markersize=6)
    ax1.set_title('Nodos explorados')
    ax1.set_xlabel('Profundidad')
    ax1.set_ylabel('Nodos (escala log)')
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax1.set_xticks(depths)
    ax1.grid(True, which='both', linestyle='--', alpha=0.4)

    ax2.plot(depths, times, 's--', color='#1D9E75', linewidth=2, markersize=6)
    ax2.set_title('Tiempo de ejecución')
    ax2.set_xlabel('Profundidad')
    ax2.set_ylabel('Tiempo (s)')
    ax2.set_xticks(depths)
    ax2.grid(True, linestyle='--', alpha=0.4)

    plt.tight_layout()
    plt.savefig('a2_alphabeta3.png', dpi=150, bbox_inches='tight')
    print("  Guardada: a2_alphabeta3.png\n")
    plt.show()


def seccion_b():
    #(b) Búsqueda alpha-beta en 4x4, depth 1-6.
    #Registra nodos visitados, tiempo de ejecución y factor de ramificación efectivo.
    print("(b) Alpha-β 4x4 — depth 1 a 6")
    resultados = bench_alpha_beta(size=4, depths=range(1, 7))

    print(f"{'Depth':>6} {'Nodos':>12} {'Tiempo (s)':>12} {'EBF':>10}")
    for d, n, t, ebf in resultados:
        print(f"{d:>6} {n:>12,} {t:>12.6f} {ebf:>10.4f}")

    depths = [r[0] for r in resultados]
    nodes  = [r[1] for r in resultados]
    times  = [r[2] for r in resultados]
    ebfs   = [r[3] for r in resultados]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('(b) Alpha-β — Tic-Tac-Toe 4×4', fontsize=13, fontweight='bold')

    ax1.semilogy(depths, nodes, 'o-', color='#378ADD', linewidth=2, markersize=6)
    ax1.set_title('Nodos explorados')
    ax1.set_xlabel('Profundidad')
    ax1.set_ylabel('Nodos (escala log)')
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax1.set_xticks(depths)
    ax1.grid(True, which='both', linestyle='--', alpha=0.4)

    ax2.plot(depths, times, 's-', color='#378ADD', linewidth=2, markersize=6)
    ax2.set_title('Tiempo de ejecución')
    ax2.set_xlabel('Profundidad')
    ax2.set_ylabel('Tiempo (s)')
    ax2.set_xticks(depths)
    ax2.grid(True, linestyle='--', alpha=0.4)

    ax3.plot(depths, ebfs, '^-', color='#BA7517', linewidth=2, markersize=6)
    ax3.set_title('Factor de ramificación efectivo')
    ax3.set_xlabel('Profundidad')
    ax3.set_ylabel(r'$\sqrt[d]{nodos}$')
    ax3.set_xticks(depths)
    ax3.grid(True, linestyle='--', alpha=0.4)

    plt.tight_layout()
    plt.savefig('b_alphabeta4.png', dpi=150, bbox_inches='tight')
    print("  Guardada: b_alphabeta4.png\n")
    plt.show()


#Bloque de ejecución principal. Corre las tres secciones del experimento en orden.
if __name__ == "__main__":
    seccion_a1()
    seccion_a2()
    seccion_b()