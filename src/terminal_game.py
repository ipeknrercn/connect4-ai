"""
Terminal Game Mode
------------------
Text-based gameplay for environments without pygame.
Also provides an AI vs AI mode where two agents at different
depths play each other - useful for demonstrating that deeper
search produces stronger play.

Usage:
    python terminal_game.py           # Human vs AI (default)
    python terminal_game.py ai_vs_ai  # AI vs AI demo
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from board import Connect4Board, PLAYER_1, PLAYER_2
from ai_agent import AIAgent


def print_board(board: Connect4Board):
    print()
    print(board)
    print()


def human_vs_ai(difficulty: str = "medium"):
    board = Connect4Board()
    agent = AIAgent.from_difficulty(difficulty)

    print(f"\n=== Connect 4 - Human (X) vs AI (O) [{difficulty}] ===")
    print_board(board)

    while not board.is_terminal():
        # Human turn
        valid = board.get_valid_moves()
        while True:
            try:
                move = int(input(f"Your move (columns {valid}): "))
                if move in valid:
                    break
            except ValueError:
                pass
            print("Invalid input, try again.")

        board.drop_piece(move, PLAYER_1)
        print_board(board)

        if board.check_win(PLAYER_1):
            print(">>> You won! <<<")
            return
        if board.is_full():
            print(">>> Draw! <<<")
            return

        # AI turn
        print("AI is thinking...")
        stats = agent.choose_move(board)
        print(
            f"AI plays column {stats.best_move}  "
            f"(nodes: {stats.nodes_visited:,}, "
            f"pruned: {stats.pruned_branches:,}, "
            f"time: {stats.elapsed_seconds:.2f}s)"
        )
        board.drop_piece(stats.best_move, PLAYER_2)
        print_board(board)

        if board.check_win(PLAYER_2):
            print(">>> AI won! <<<")
            return
        if board.is_full():
            print(">>> Draw! <<<")
            return


def ai_vs_ai(depth_x: int = 2, depth_o: int = 5):
    """
    Two AIs at different search depths play each other.
    The deeper agent should (almost) always win, demonstrating
    the value of deeper search.
    """
    board = Connect4Board()
    agent_x = AIAgent(ai_player=PLAYER_1, depth=depth_x, use_pruning=True)
    agent_o = AIAgent(ai_player=PLAYER_2, depth=depth_o, use_pruning=True)

    print(f"\n=== AI vs AI: X (depth {depth_x}) vs O (depth {depth_o}) ===")
    print_board(board)

    turn = PLAYER_1
    while not board.is_terminal():
        agent = agent_x if turn == PLAYER_1 else agent_o
        stats = agent.choose_move(board)
        print(
            f"Player {turn} -> column {stats.best_move}  "
            f"[nodes: {stats.nodes_visited:,}, "
            f"time: {stats.elapsed_seconds:.2f}s]"
        )
        board.drop_piece(stats.best_move, turn)
        print_board(board)
        turn = PLAYER_2 if turn == PLAYER_1 else PLAYER_1

    if board.check_win(PLAYER_1):
        print(f">>> Player X (depth {depth_x}) won! <<<")
    elif board.check_win(PLAYER_2):
        print(f">>> Player O (depth {depth_o}) won! <<<")
    else:
        print(">>> Draw! <<<")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "ai_vs_ai":
        ai_vs_ai()
    else:
        difficulty = sys.argv[1] if len(sys.argv) > 1 else "medium"
        human_vs_ai(difficulty)
