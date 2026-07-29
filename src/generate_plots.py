"""Generate visualization plots for the benchmark results (for the report)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from board import Connect4Board, PLAYER_1, PLAYER_2
from ai_agent import AIAgent


def collect_data(max_depth: int = 5):
    """Re-run the benchmark on the empty board and return arrays for plotting."""
    depths = list(range(1, max_depth + 1))
    mm_nodes, ab_nodes = [], []
    mm_times, ab_times = [], []

    for d in depths:
        board = Connect4Board()
        mm = AIAgent(depth=d, use_pruning=False).choose_move(board.copy())
        ab = AIAgent(depth=d, use_pruning=True).choose_move(board.copy())
        mm_nodes.append(mm.nodes_visited)
        ab_nodes.append(ab.nodes_visited)
        mm_times.append(mm.elapsed_seconds)
        ab_times.append(ab.elapsed_seconds)

    return depths, mm_nodes, ab_nodes, mm_times, ab_times


def main():
    print("Collecting benchmark data for plots...")
    depths, mm_nodes, ab_nodes, mm_times, ab_times = collect_data(max_depth=5)

    os.makedirs("/home/claude/connect4_ai/assets", exist_ok=True)

    # --- Plot 1: Nodes visited (log scale) ---
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(depths, mm_nodes, marker="o", linewidth=2.5,
            label="Plain Minimax", color="#e74c3c")
    ax.plot(depths, ab_nodes, marker="s", linewidth=2.5,
            label="Alpha-Beta Pruning", color="#2ecc71")
    ax.set_yscale("log")
    ax.set_xlabel("Search Depth", fontsize=12)
    ax.set_ylabel("Nodes Visited (log scale)", fontsize=12)
    ax.set_title("Minimax vs Alpha-Beta: Search Tree Size",
                 fontsize=13, fontweight="bold")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=11)
    for d, n in zip(depths, mm_nodes):
        ax.annotate(f"{n:,}", (d, n), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=9, color="#c0392b")
    for d, n in zip(depths, ab_nodes):
        ax.annotate(f"{n:,}", (d, n), textcoords="offset points",
                    xytext=(0, -15), ha="center", fontsize=9, color="#27ae60")
    plt.tight_layout()
    plt.savefig("/home/claude/connect4_ai/assets/nodes_comparison.png", dpi=140)
    plt.close()

    # --- Plot 2: Time comparison ---
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(depths))
    width = 0.35
    ax.bar(x - width/2, mm_times, width, label="Plain Minimax", color="#e74c3c")
    ax.bar(x + width/2, ab_times, width, label="Alpha-Beta Pruning", color="#2ecc71")
    ax.set_xlabel("Search Depth", fontsize=12)
    ax.set_ylabel("Time (seconds)", fontsize=12)
    ax.set_title("Computation Time Comparison",
                 fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(depths)
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(fontsize=11)
    for i, (m, a) in enumerate(zip(mm_times, ab_times)):
        ax.text(i - width/2, m + max(mm_times)*0.01, f"{m:.2f}s",
                ha="center", fontsize=9)
        ax.text(i + width/2, a + max(mm_times)*0.01, f"{a:.2f}s",
                ha="center", fontsize=9)
    plt.tight_layout()
    plt.savefig("/home/claude/connect4_ai/assets/time_comparison.png", dpi=140)
    plt.close()

    # --- Plot 3: Speedup ratio ---
    speedups = [m / a if a > 0 else 0 for m, a in zip(mm_nodes, ab_nodes)]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(depths, speedups, color="#3498db", edgecolor="#2c3e50")
    ax.set_xlabel("Search Depth", fontsize=12)
    ax.set_ylabel("Speedup Factor (Minimax / Alpha-Beta)", fontsize=12)
    ax.set_title("Alpha-Beta Pruning Speedup over Plain Minimax",
                 fontsize=13, fontweight="bold")
    ax.grid(True, axis="y", alpha=0.3)
    for bar, s in zip(bars, speedups):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{s:.2f}x", ha="center", fontsize=11, fontweight="bold")
    plt.tight_layout()
    plt.savefig("/home/claude/connect4_ai/assets/speedup.png", dpi=140)
    plt.close()

    print("Plots saved to assets/")
    print(f"  Speedup at depth 5: {speedups[-1]:.2f}x")


if __name__ == "__main__":
    main()
