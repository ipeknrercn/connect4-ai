"""
AI Agent: Minimax with optional Alpha-Beta Pruning
---------------------------------------------------

Minimax is a recursive algorithm that assumes both players play optimally.
- MAX player (the AI) tries to maximize the evaluation score.
- MIN player (the opponent) tries to minimize it.

The algorithm explores the game tree up to a fixed DEPTH, then
uses the heuristic evaluator for leaf (non-terminal) nodes.

Alpha-Beta Pruning is an optimization that tracks two bounds:
    alpha = best already-explored value for the MAX player
    beta  = best already-explored value for the MIN player
When alpha >= beta, we can "prune" the rest of that branch because
the opponent would never allow the current player to reach it.

We implement BOTH versions so the report can quantify the speedup
(typically 5-20x fewer nodes explored).

Key implementation choices:
    1. Column ordering: We try the center column first, then expand
       outward. Since the center is usually the best move, this
       maximizes Alpha-Beta's pruning effectiveness.
    2. Immediate win/loss detection: Before recursing, we check for
       terminal states to avoid wasted computation.
    3. Node counting: Each call increments a counter so we can report
       search size for the benchmark.

Author: Ipek
"""

import math
import random
import time
from dataclasses import dataclass, field
from typing import Optional, Tuple

from board import Connect4Board, COLS, PLAYER_1, PLAYER_2
from evaluator import evaluate_position, SCORE_WIN, SCORE_LOSS


@dataclass
class SearchStats:
    """Tracks performance metrics for one AI move computation."""
    nodes_visited: int = 0      # Total recursive calls
    pruned_branches: int = 0    # Alpha-Beta cutoffs (0 for plain minimax)
    elapsed_seconds: float = 0.0
    best_score: int = 0
    best_move: int = -1
    depth_used: int = 0
    algorithm: str = ""         # "minimax" or "alphabeta"


def _ordered_columns(valid_moves) -> list:
    """
    Return valid moves ordered from center outward.
    Example for COLS=7: [3, 2, 4, 1, 5, 0, 6]

    This helps Alpha-Beta prune earlier because good moves are
    explored first (center is typically strongest in Connect 4).
    """
    center = COLS // 2
    # Sort by distance from center, preserving valid_moves only
    return sorted(valid_moves, key=lambda c: abs(c - center))


# ---------------------------------------------------------------
# Plain Minimax (no pruning) - for benchmarking comparison
# ---------------------------------------------------------------
def minimax(
    board: Connect4Board,
    depth: int,
    maximizing: bool,
    ai_player: int,
    stats: SearchStats,
) -> Tuple[Optional[int], int]:
    """
    Plain Minimax without pruning.
    Returns (best_column, best_score).
    """
    stats.nodes_visited += 1

    valid_moves = board.get_valid_moves()
    opponent = PLAYER_1 if ai_player == PLAYER_2 else PLAYER_2

    # ---- Terminal check ----
    if board.check_win(ai_player):
        return (None, SCORE_WIN + depth)   # Prefer faster wins
    if board.check_win(opponent):
        return (None, SCORE_LOSS - depth)  # Delay losses
    if len(valid_moves) == 0:
        return (None, 0)  # Draw
    if depth == 0:
        return (None, evaluate_position(board, ai_player))

    if maximizing:
        best_score = -math.inf
        best_col = random.choice(valid_moves)
        for col in _ordered_columns(valid_moves):
            row = board.get_next_open_row(col)
            board.grid[row][col] = ai_player
            _, score = minimax(board, depth - 1, False, ai_player, stats)
            board.grid[row][col] = 0  # undo
            if score > best_score:
                best_score = score
                best_col = col
        return best_col, best_score
    else:
        best_score = math.inf
        best_col = random.choice(valid_moves)
        for col in _ordered_columns(valid_moves):
            row = board.get_next_open_row(col)
            board.grid[row][col] = opponent
            _, score = minimax(board, depth - 1, True, ai_player, stats)
            board.grid[row][col] = 0
            if score < best_score:
                best_score = score
                best_col = col
        return best_col, best_score


# ---------------------------------------------------------------
# Minimax with Alpha-Beta Pruning (the main algorithm)
# ---------------------------------------------------------------
def alphabeta(
    board: Connect4Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing: bool,
    ai_player: int,
    stats: SearchStats,
) -> Tuple[Optional[int], float]:
    """
    Minimax with Alpha-Beta Pruning.
    Returns (best_column, best_score).

    Parameters:
        alpha : best score the MAXIMIZER can guarantee so far
        beta  : best score the MINIMIZER can guarantee so far
    Invariant: if alpha >= beta, the current branch is pruned.
    """
    stats.nodes_visited += 1

    valid_moves = board.get_valid_moves()
    opponent = PLAYER_1 if ai_player == PLAYER_2 else PLAYER_2

    # ---- Terminal / depth cutoff ----
    if board.check_win(ai_player):
        return (None, SCORE_WIN + depth)
    if board.check_win(opponent):
        return (None, SCORE_LOSS - depth)
    if len(valid_moves) == 0:
        return (None, 0)
    if depth == 0:
        return (None, evaluate_position(board, ai_player))

    if maximizing:
        value = -math.inf
        best_col = random.choice(valid_moves)
        for col in _ordered_columns(valid_moves):
            row = board.get_next_open_row(col)
            board.grid[row][col] = ai_player
            _, new_score = alphabeta(
                board, depth - 1, alpha, beta, False, ai_player, stats
            )
            board.grid[row][col] = 0

            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                # Prune: opponent won't let us reach this branch
                stats.pruned_branches += 1
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_moves)
        for col in _ordered_columns(valid_moves):
            row = board.get_next_open_row(col)
            board.grid[row][col] = opponent
            _, new_score = alphabeta(
                board, depth - 1, alpha, beta, True, ai_player, stats
            )
            board.grid[row][col] = 0

            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                stats.pruned_branches += 1
                break
        return best_col, value


# ---------------------------------------------------------------
# Public interface: AIAgent class
# ---------------------------------------------------------------
class AIAgent:
    """
    Wraps a search algorithm with a specified depth.
    Difficulty levels (for UI):
        Easy   : depth 2
        Medium : depth 4
        Hard   : depth 6
    """

    DIFFICULTY_MAP = {
        "easy": 2,
        "medium": 4,
        "hard": 6,
    }

    def __init__(
        self,
        ai_player: int = PLAYER_2,
        depth: int = 4,
        use_pruning: bool = True,
    ):
        self.ai_player = ai_player
        self.depth = depth
        self.use_pruning = use_pruning

    @classmethod
    def from_difficulty(cls, difficulty: str, ai_player: int = PLAYER_2) -> "AIAgent":
        depth = cls.DIFFICULTY_MAP.get(difficulty.lower(), 4)
        return cls(ai_player=ai_player, depth=depth, use_pruning=True)

    def choose_move(self, board: Connect4Board) -> SearchStats:
        """
        Compute the best move for the current board state.
        Returns a SearchStats object containing the chosen move and
        performance metrics.
        """
        stats = SearchStats(
            depth_used=self.depth,
            algorithm="alphabeta" if self.use_pruning else "minimax",
        )

        start = time.perf_counter()

        if self.use_pruning:
            best_col, best_score = alphabeta(
                board, self.depth, -math.inf, math.inf, True, self.ai_player, stats
            )
        else:
            best_col, best_score = minimax(
                board, self.depth, True, self.ai_player, stats
            )

        stats.elapsed_seconds = time.perf_counter() - start
        stats.best_move = best_col if best_col is not None else -1
        stats.best_score = int(best_score) if best_score != math.inf else 0

        return stats
