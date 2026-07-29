"""
Connect 4 Board Module
----------------------
Handles all game state, rules, and win-detection logic.
Separated from AI logic for clarity and testability.

Board representation:
    - 6 rows x 7 columns (standard Connect 4 dimensions)
    - NumPy 2D array for fast slicing (used in win checks & evaluation)
    - 0 = empty, 1 = Player 1, 2 = Player 2

Author: Ipek
Course: SWE - Artificial Intelligence
"""

import numpy as np
from typing import List, Optional, Tuple


# ---- Board constants ----
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER_1 = 1   # Human (in Human vs AI mode)
PLAYER_2 = 2   # AI
CONNECT = 4    # Number in a row needed to win


class Connect4Board:
    """
    Represents the state of a Connect 4 game.

    Pieces fall to the lowest empty row of a column (gravity).
    We store the board as a NumPy array where row 0 is the TOP
    and row 5 is the BOTTOM. When a piece is dropped into column c,
    it occupies the lowest empty row in that column.
    """

    def __init__(self, grid: Optional[np.ndarray] = None):
        # If a grid is passed, copy it (used for simulating future states in AI)
        if grid is not None:
            self.grid = grid.copy()
        else:
            self.grid = np.zeros((ROWS, COLS), dtype=np.int8)

        # Track move history for potential undo / replay features
        self.move_history: List[int] = []

    # ---------------------------------------------------------------
    # Core mechanics
    # ---------------------------------------------------------------
    def get_valid_moves(self) -> List[int]:
        """Return list of columns (0..6) that are not yet full."""
        # A column is valid if its TOP cell (row 0) is empty
        return [c for c in range(COLS) if self.grid[0][c] == EMPTY]

    def is_valid_move(self, col: int) -> bool:
        """Check if a specific column can accept a new piece."""
        return 0 <= col < COLS and self.grid[0][col] == EMPTY

    def get_next_open_row(self, col: int) -> Optional[int]:
        """
        Return the row index where a piece would land in the given column.
        Simulates gravity: scans from bottom (row 5) upward.
        Returns None if the column is full.
        """
        for r in range(ROWS - 1, -1, -1):
            if self.grid[r][col] == EMPTY:
                return r
        return None

    def drop_piece(self, col: int, player: int) -> bool:
        """
        Drop a piece for `player` into column `col`.
        Returns True if successful, False if the column is invalid/full.
        """
        if not self.is_valid_move(col):
            return False

        row = self.get_next_open_row(col)
        if row is None:
            return False

        self.grid[row][col] = player
        self.move_history.append(col)
        return True

    def undo_last_move(self) -> None:
        """Undo the most recent move (used during AI simulation)."""
        if not self.move_history:
            return
        col = self.move_history.pop()
        # Find the TOPMOST filled cell in that column and clear it
        for r in range(ROWS):
            if self.grid[r][col] != EMPTY:
                self.grid[r][col] = EMPTY
                return

    def is_full(self) -> bool:
        """True if the entire board is filled (draw condition)."""
        return len(self.get_valid_moves()) == 0

    # ---------------------------------------------------------------
    # Win detection
    # ---------------------------------------------------------------
    def check_win(self, player: int) -> bool:
        """
        Return True if `player` has four-in-a-row anywhere on the board.
        Checks horizontal, vertical, and both diagonal directions.
        Implemented with explicit loops for clarity (easy to explain in report).
        """
        # 1) Horizontal check (any 4 consecutive cells in a row)
        for r in range(ROWS):
            for c in range(COLS - CONNECT + 1):
                if all(self.grid[r][c + i] == player for i in range(CONNECT)):
                    return True

        # 2) Vertical check
        for c in range(COLS):
            for r in range(ROWS - CONNECT + 1):
                if all(self.grid[r + i][c] == player for i in range(CONNECT)):
                    return True

        # 3) Diagonal "/" (bottom-left to top-right)
        for r in range(CONNECT - 1, ROWS):
            for c in range(COLS - CONNECT + 1):
                if all(self.grid[r - i][c + i] == player for i in range(CONNECT)):
                    return True

        # 4) Diagonal "\" (top-left to bottom-right)
        for r in range(ROWS - CONNECT + 1):
            for c in range(COLS - CONNECT + 1):
                if all(self.grid[r + i][c + i] == player for i in range(CONNECT)):
                    return True

        return False

    def get_winning_positions(self, player: int) -> Optional[List[Tuple[int, int]]]:
        """
        If `player` has won, return the list of 4 (row, col) positions
        that make up the winning line. Useful for highlighting in the GUI.
        """
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - CONNECT + 1):
                if all(self.grid[r][c + i] == player for i in range(CONNECT)):
                    return [(r, c + i) for i in range(CONNECT)]
        # Vertical
        for c in range(COLS):
            for r in range(ROWS - CONNECT + 1):
                if all(self.grid[r + i][c] == player for i in range(CONNECT)):
                    return [(r + i, c) for i in range(CONNECT)]
        # Diagonal /
        for r in range(CONNECT - 1, ROWS):
            for c in range(COLS - CONNECT + 1):
                if all(self.grid[r - i][c + i] == player for i in range(CONNECT)):
                    return [(r - i, c + i) for i in range(CONNECT)]
        # Diagonal \
        for r in range(ROWS - CONNECT + 1):
            for c in range(COLS - CONNECT + 1):
                if all(self.grid[r + i][c + i] == player for i in range(CONNECT)):
                    return [(r + i, c + i) for i in range(CONNECT)]
        return None

    def is_terminal(self) -> bool:
        """Terminal state = someone won OR board full."""
        return (
            self.check_win(PLAYER_1)
            or self.check_win(PLAYER_2)
            or self.is_full()
        )

    # ---------------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------------
    def copy(self) -> "Connect4Board":
        """Return a deep copy of the board (used in AI tree search)."""
        new_board = Connect4Board(self.grid)
        new_board.move_history = self.move_history.copy()
        return new_board

    def __str__(self) -> str:
        """Pretty-print for terminal mode."""
        symbols = {EMPTY: ".", PLAYER_1: "X", PLAYER_2: "O"}
        lines = []
        for row in self.grid:
            lines.append(" ".join(symbols[cell] for cell in row))
        lines.append(" ".join(str(i) for i in range(COLS)))  # column labels
        return "\n".join(lines)
