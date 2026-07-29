"""
Benchmark: Plain Minimax vs Alpha-Beta Pruning
----------------------------------------------
Produces quantitative evidence of Alpha-Beta's speedup for the report.

We run both algorithms on IDENTICAL board positions at increasing
search depths, measuring:
    - nodes visited (tree size)
    - elapsed time
    - branches pruned (alpha-beta only)

The ratio (minimax_nodes / alphabeta_nodes) demonstrates how aggressively
Alpha-Beta eliminates provably-suboptimal branches without changing the
final move choice (both algorithms find the same optimal move).

Run:
    python benchmark.py
"""

import sys
import os

# Allow running as a standalone script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from board import Connect4Board, PLAYER_1, PLAYER_2
from ai_agent import AIAgent


def create_test_positions() -> list:
    """Return a list of (name, board) test positions at varying complexity."""
    positions = []

    # --- Position 1: Empty board (most branching) ---
    b1 = Connect4Board()
    positions.append(("Empty board", b1))

    # --- Position 2: Early game, 4 moves played ---
    b2 = Connect4Board()
    for col, player in [(3, PLAYER_1), (3, PLAYER_2), (4, PLAYER_1), (2, PLAYER_2)]:
        b2.drop_piece(col, player)
    positions.append(("Early game (4 moves)", b2))

    # --- Position 3: Mid-game, 8 moves played (no winner yet) ---
    b3 = Connect4Board()
    moves = [
        (3, PLAYER_1), (2, PLAYER_2), (4, PLAYER_1), (3, PLAYER_2),
        (2, PLAYER_1), (4, PLAYER_2), (1, PLAYER_1), (5, PLAYER_2),
    ]
    for col, player in moves:
        b3.drop_piece(col, player)
    positions.append(("Mid-game (8 moves)", b3))

    return positions


def run_benchmark(max_depth: int = 5):
    """
    Run minimax vs alpha-beta on each test position at depths 1..max_depth.
    Prints a formatted table suitable for inclusion in the report.
    """
    positions = create_test_positions()
    results = []

    header = (
        f"{'Position':<22} {'Depth':<6} "
        f"{'Minimax Nodes':>15} {'AB Nodes':>12} "
        f"{'Speedup':>10} {'MM Time':>10} {'AB Time':>10}"
    )
    print("=" * len(header))
    print(header)
    print("=" * len(header))

    for name, board in positions:
        for depth in range(1, max_depth + 1):
            # Plain minimax
            mm_agent = AIAgent(depth=depth, use_pruning=False)
            mm_stats = mm_agent.choose_move(board.copy())

            # Alpha-beta
            ab_agent = AIAgent(depth=depth, use_pruning=True)
            ab_stats = ab_agent.choose_move(board.copy())

            speedup = (
                mm_stats.nodes_visited / ab_stats.nodes_visited
                if ab_stats.nodes_visited > 0 else 0
            )

            print(
                f"{name:<22} {depth:<6} "
                f"{mm_stats.nodes_visited:>15,} {ab_stats.nodes_visited:>12,} "
                f"{speedup:>9.2f}x "
                f"{mm_stats.elapsed_seconds:>9.3f}s "
                f"{ab_stats.elapsed_seconds:>9.3f}s"
            )

            results.append({
                "position": name,
                "depth": depth,
                "minimax_nodes": mm_stats.nodes_visited,
                "alphabeta_nodes": ab_stats.nodes_visited,
                "speedup": speedup,
                "minimax_time": mm_stats.elapsed_seconds,
                "alphabeta_time": ab_stats.elapsed_seconds,
                "minimax_move": mm_stats.best_move,
                "alphabeta_move": ab_stats.best_move,
            })

        print("-" * len(header))

    # Verify that both algorithms chose the same moves (sanity check)
    print("\nSanity check: Do minimax and alpha-beta agree on the best move?")
    mismatches = [r for r in results if r["minimax_move"] != r["alphabeta_move"]]
    if mismatches:
        print(f"  WARNING: {len(mismatches)} disagreements (may be due to ties)")
    else:
        print("  YES - both algorithms always chose the same column (as expected).")

    return results


if __name__ == "__main__":
    print("\nConnect 4 AI - Minimax vs Alpha-Beta Benchmark")
    print("Course: SWE - Artificial Intelligence\n")
    run_benchmark(max_depth=5)
