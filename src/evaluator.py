"""
Heuristic Evaluation Function for Connect 4
-------------------------------------------
Connect 4's game tree has ~4.5 trillion positions, so Minimax
cannot reach terminal states at reasonable depths. We therefore
evaluate non-terminal positions with a heuristic score.

Heuristic design (explained in report):
    1. Center column preference: pieces in the center column have
       the most potential 4-in-a-row lines passing through them,
       so we reward them.
    2. Window scoring: slide a 4-cell "window" over every possible
       line (horizontal, vertical, 2 diagonals) and score each
       window based on piece configuration.

Window scores (for the AI player):
    +100   : 4 AI pieces (winning position)
    + 10   : 3 AI pieces + 1 empty (one move away from winning)
    +  5   : 2 AI pieces + 2 empty (developing threat)
    -  8   : 3 opponent pieces + 1 empty (must block!)
              Slightly less than +10 so AI prefers offense when tied.

Reference: Heuristics inspired by classic "Connect 4 solved"
literature (Allis, 1988) and common open-source implementations.

Author: Ipek
"""

import numpy as np
from board import Connect4Board, ROWS, COLS, CONNECT, EMPTY, PLAYER_1, PLAYER_2


# Scoring constants - tuned empirically
SCORE_WIN = 100000       # Terminal: AI wins
SCORE_LOSS = -100000     # Terminal: AI loses
SCORE_FOUR = 100         # 4 in a row (should already be caught as terminal)
SCORE_THREE = 10         # 3 in a row + 1 empty
SCORE_TWO = 5            # 2 in a row + 2 empty
SCORE_BLOCK_THREE = -8   # Opponent has 3 in a row + 1 empty
SCORE_BLOCK_TWO = -2     # Opponent has 2 in a row + 2 empty
CENTER_BONUS = 3         # Per piece in the center column


def evaluate_window(window: np.ndarray, ai_player: int) -> int:
    """
    Score a 4-cell window from the AI's perspective.
    """
    opponent = PLAYER_1 if ai_player == PLAYER_2 else PLAYER_2

    ai_count = int(np.sum(window == ai_player))
    opp_count = int(np.sum(window == opponent))
    empty_count = int(np.sum(window == EMPTY))

    # If both players have pieces in this window, no one can complete it.
    # It contributes 0 to the score.
    if ai_count > 0 and opp_count > 0:
        return 0

    score = 0

    # AI's threats
    if ai_count == 4:
        score += SCORE_FOUR
    elif ai_count == 3 and empty_count == 1:
        score += SCORE_THREE
    elif ai_count == 2 and empty_count == 2:
        score += SCORE_TWO

    # Opponent's threats (defensive scoring)
    if opp_count == 3 and empty_count == 1:
        score += SCORE_BLOCK_THREE
    elif opp_count == 2 and empty_count == 2:
        score += SCORE_BLOCK_TWO

    return score


def evaluate_position(board: Connect4Board, ai_player: int) -> int:
    """
    Compute the heuristic score of a non-terminal board position.
    Higher = better for AI.

    We enumerate every possible 4-cell line on the board
    (horizontal, vertical, both diagonals) and sum their window scores.
    """
    # First check terminal conditions
    opponent = PLAYER_1 if ai_player == PLAYER_2 else PLAYER_2
    if board.check_win(ai_player):
        return SCORE_WIN
    if board.check_win(opponent):
        return SCORE_LOSS

    grid = board.grid
    score = 0

    # ---- Center column bonus ----
    # The center column is strategically the most valuable because
    # the most 4-in-a-row lines pass through it.
    center_col = grid[:, COLS // 2]
    score += int(np.sum(center_col == ai_player)) * CENTER_BONUS

    # ---- Horizontal windows ----
    for r in range(ROWS):
        row = grid[r, :]
        for c in range(COLS - CONNECT + 1):
            window = row[c : c + CONNECT]
            score += evaluate_window(window, ai_player)

    # ---- Vertical windows ----
    for c in range(COLS):
        col = grid[:, c]
        for r in range(ROWS - CONNECT + 1):
            window = col[r : r + CONNECT]
            score += evaluate_window(window, ai_player)

    # ---- Diagonal "\" windows (top-left to bottom-right) ----
    for r in range(ROWS - CONNECT + 1):
        for c in range(COLS - CONNECT + 1):
            window = np.array([grid[r + i][c + i] for i in range(CONNECT)])
            score += evaluate_window(window, ai_player)

    # ---- Diagonal "/" windows (bottom-left to top-right) ----
    for r in range(CONNECT - 1, ROWS):
        for c in range(COLS - CONNECT + 1):
            window = np.array([grid[r - i][c + i] for i in range(CONNECT)])
            score += evaluate_window(window, ai_player)

    return score
