"""
Pygame GUI for Connect 4 AI
---------------------------
Visual interface for Human vs AI and AI vs AI games.

Features:
    - Click a column to drop your piece (or hover to preview)
    - Live display of AI's search stats (nodes, time, pruning)
    - Winning line is highlighted in gold
    - Difficulty selector on the start screen (Easy / Medium / Hard)
    - "New Game" button after the match ends

Controls:
    - Left-click   : drop piece in that column
    - R            : restart game
    - ESC          : return to menu

Author: Ipek
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from board import Connect4Board, ROWS, COLS, PLAYER_1, PLAYER_2, EMPTY
from ai_agent import AIAgent, SearchStats


# ----- Visual constants -----
SQUARE_SIZE = 90
RADIUS = SQUARE_SIZE // 2 - 6
BOARD_WIDTH = COLS * SQUARE_SIZE
BOARD_HEIGHT = ROWS * SQUARE_SIZE
TOP_BAR = SQUARE_SIZE         # Top area for piece-drop preview
SIDE_PANEL = 300              # Right panel for AI stats
WINDOW_WIDTH = BOARD_WIDTH + SIDE_PANEL
WINDOW_HEIGHT = BOARD_HEIGHT + TOP_BAR

# ----- Colors (vibrant palette) -----
BG_COLOR = (20, 24, 48)             # Deep navy
BOARD_COLOR = (30, 144, 255)        # Vibrant electric blue
EMPTY_COLOR = (15, 20, 40)          # Darker holes for contrast
PLAYER_1_COLOR = (255, 71, 87)      # Vivid red
PLAYER_2_COLOR = (255, 215, 0)      # Bright gold/yellow
TEXT_COLOR = (245, 246, 255)
PANEL_COLOR = (28, 32, 58)
HIGHLIGHT_COLOR = (50, 255, 126)    # Neon green for winning line
BUTTON_COLOR = (88, 101, 242)       # Vibrant indigo
BUTTON_HOVER = (124, 138, 255)      # Lighter indigo on hover
ACCENT_COLOR = (255, 107, 157)      # Hot pink accent
INFO_COLOR = (180, 200, 255)        # Soft blue for info text


class Connect4GUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Connect 4 AI - Minimax & Alpha-Beta")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_large = pygame.font.SysFont("arial", 36, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.font_tiny = pygame.font.SysFont("arial", 14)

        self.board = Connect4Board()
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.current_player = PLAYER_1  # Human goes first by convention
        self.ai_agent: AIAgent = AIAgent.from_difficulty("medium")
        self.last_stats: SearchStats = None
        self.status_message = "Your turn - click a column"
        self.difficulty = "medium"

    # -----------------------------------------------------------------
    # Drawing
    # -----------------------------------------------------------------
    def draw_board(self):
        # Top bar (empty - piece preview area)
        pygame.draw.rect(self.screen, BG_COLOR, (0, 0, BOARD_WIDTH, TOP_BAR))

        # The board itself (blue rectangle with circular holes)
        pygame.draw.rect(
            self.screen, BOARD_COLOR,
            (0, TOP_BAR, BOARD_WIDTH, BOARD_HEIGHT)
        )

        # Draw each cell
        for r in range(ROWS):
            for c in range(COLS):
                cx = c * SQUARE_SIZE + SQUARE_SIZE // 2
                cy = TOP_BAR + r * SQUARE_SIZE + SQUARE_SIZE // 2
                piece = self.board.grid[r][c]
                if piece == EMPTY:
                    color = EMPTY_COLOR
                elif piece == PLAYER_1:
                    color = PLAYER_1_COLOR
                else:
                    color = PLAYER_2_COLOR
                pygame.draw.circle(self.screen, color, (cx, cy), RADIUS)

        # Highlight winning line if any
        if self.winning_line:
            for (r, c) in self.winning_line:
                cx = c * SQUARE_SIZE + SQUARE_SIZE // 2
                cy = TOP_BAR + r * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.circle(
                    self.screen, HIGHLIGHT_COLOR, (cx, cy), RADIUS, width=5
                )

    def draw_hover_piece(self, mouse_x: int):
        """Show a translucent piece above the column the mouse is over."""
        if self.game_over or self.current_player != PLAYER_1:
            return
        if mouse_x >= BOARD_WIDTH:
            return
        col = mouse_x // SQUARE_SIZE
        if self.board.is_valid_move(col):
            cx = col * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(
                self.screen, PLAYER_1_COLOR,
                (cx, TOP_BAR // 2), RADIUS
            )

    def draw_side_panel(self):
        """Right panel: AI stats + controls."""
        panel_x = BOARD_WIDTH
        pygame.draw.rect(
            self.screen, PANEL_COLOR,
            (panel_x, 0, SIDE_PANEL, WINDOW_HEIGHT)
        )

        y = 20
        # Title
        title = self.font_medium.render("AI Statistics", True, TEXT_COLOR)
        self.screen.blit(title, (panel_x + 20, y))
        y += 40

        # Difficulty indicator
        diff_text = self.font_small.render(
            f"Difficulty: {self.difficulty.upper()} "
            f"(depth {self.ai_agent.depth})",
            True, TEXT_COLOR
        )
        self.screen.blit(diff_text, (panel_x + 20, y))
        y += 30

        algo_text = self.font_small.render(
            f"Algorithm: Alpha-Beta",
            True, TEXT_COLOR
        )
        self.screen.blit(algo_text, (panel_x + 20, y))
        y += 40

        # Last move stats
        if self.last_stats:
            lines = [
                f"Last AI move: column {self.last_stats.best_move}",
                f"Score: {self.last_stats.best_score}",
                f"Nodes visited: {self.last_stats.nodes_visited:,}",
                f"Branches pruned: {self.last_stats.pruned_branches:,}",
                f"Think time: {self.last_stats.elapsed_seconds:.3f}s",
            ]
            for line in lines:
                surf = self.font_small.render(line, True, TEXT_COLOR)
                self.screen.blit(surf, (panel_x + 20, y))
                y += 26

        # Status message (bottom of panel)
        y = WINDOW_HEIGHT - 140
        pygame.draw.line(
            self.screen, (70, 70, 90),
            (panel_x + 10, y - 10),
            (panel_x + SIDE_PANEL - 10, y - 10), 2
        )

        status_surf = self.font_small.render(self.status_message, True, TEXT_COLOR)
        self.screen.blit(status_surf, (panel_x + 20, y))
        y += 30

        # Controls hint
        hints = ["R: restart game", "ESC: main menu"]
        for h in hints:
            surf = self.font_tiny.render(h, True, (160, 160, 180))
            self.screen.blit(surf, (panel_x + 20, y))
            y += 20

    def render(self):
        self.screen.fill(BG_COLOR)
        self.draw_board()
        mouse_x, _ = pygame.mouse.get_pos()
        self.draw_hover_piece(mouse_x)
        self.draw_side_panel()
        pygame.display.flip()

    # -----------------------------------------------------------------
    # Game flow
    # -----------------------------------------------------------------
    def handle_human_move(self, mouse_x: int):
        if self.game_over or self.current_player != PLAYER_1:
            return
        if mouse_x >= BOARD_WIDTH:
            return
        col = mouse_x // SQUARE_SIZE
        if not self.board.is_valid_move(col):
            return
        self.board.drop_piece(col, PLAYER_1)

        if self.board.check_win(PLAYER_1):
            self.game_over = True
            self.winner = PLAYER_1
            self.winning_line = self.board.get_winning_positions(PLAYER_1)
            self.status_message = "You won! Press R to play again"
            return
        if self.board.is_full():
            self.game_over = True
            self.status_message = "Draw! Press R to play again"
            return

        self.current_player = PLAYER_2
        self.status_message = "AI is thinking..."

    def handle_ai_move(self):
        if self.game_over or self.current_player != PLAYER_2:
            return

        # Redraw "AI is thinking..." BEFORE the blocking compute
        self.render()

        stats = self.ai_agent.choose_move(self.board)
        self.last_stats = stats

        if stats.best_move >= 0:
            self.board.drop_piece(stats.best_move, PLAYER_2)

        if self.board.check_win(PLAYER_2):
            self.game_over = True
            self.winner = PLAYER_2
            self.winning_line = self.board.get_winning_positions(PLAYER_2)
            self.status_message = "AI won! Press R to play again"
            return
        if self.board.is_full():
            self.game_over = True
            self.status_message = "Draw! Press R to play again"
            return

        self.current_player = PLAYER_1
        self.status_message = "Your turn - click a column"

    def reset_game(self):
        self.board = Connect4Board()
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.current_player = PLAYER_1
        self.last_stats = None
        self.status_message = "Your turn - click a column"

    # -----------------------------------------------------------------
    # Start menu for difficulty selection
    # -----------------------------------------------------------------
    def show_menu(self) -> bool:
        """Return True when user picks a difficulty and starts the game."""
        buttons = [
            ("Easy (depth 2)", "easy", 0),
            ("Medium (depth 4)", "medium", 1),
            ("Hard (depth 6)", "hard", 2),
        ]
        button_rects = []
        for label, diff, i in buttons:
            rect = pygame.Rect(
                WINDOW_WIDTH // 2 - 150,
                230 + i * 70,
                300, 55
            )
            button_rects.append((rect, diff, label))

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, diff, _ in button_rects:
                        if rect.collidepoint(mouse_pos):
                            self.difficulty = diff
                            self.ai_agent = AIAgent.from_difficulty(diff)
                            self.reset_game()
                            return True

            self.screen.fill(BG_COLOR)

            # --- Title ---
            title = self.font_large.render(
                "CONNECT 4 - AI OPPONENT", True, TEXT_COLOR
            )
            self.screen.blit(
                title,
                (WINDOW_WIDTH // 2 - title.get_width() // 2, 60)
            )

            subtitle = self.font_medium.render(
                "Minimax with Alpha-Beta Pruning",
                True, ACCENT_COLOR
            )
            self.screen.blit(
                subtitle,
                (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 115)
            )

            # --- Difficulty prompt ---
            instruction = self.font_small.render(
                "Choose difficulty:", True, TEXT_COLOR
            )
            self.screen.blit(
                instruction,
                (WINDOW_WIDTH // 2 - instruction.get_width() // 2, 195)
            )

            # --- Difficulty buttons ---
            for rect, diff, label in button_rects:
                hovered = rect.collidepoint(mouse_pos)
                pygame.draw.rect(
                    self.screen,
                    BUTTON_HOVER if hovered else BUTTON_COLOR,
                    rect, border_radius=12
                )
                surf = self.font_medium.render(label, True, TEXT_COLOR)
                self.screen.blit(
                    surf,
                    (rect.centerx - surf.get_width() // 2,
                     rect.centery - surf.get_height() // 2)
                )

            # --- How to play section ---
            how_to_y = 445
            how_to_title = self.font_medium.render(
                "HOW TO PLAY", True, ACCENT_COLOR
            )
            self.screen.blit(
                how_to_title,
                (WINDOW_WIDTH // 2 - how_to_title.get_width() // 2, how_to_y)
            )

            instructions = [
                "Click a column to drop your RED disc - it falls to the bottom.",
                "The AI plays YELLOW and moves after you.",
                "First to line up 4 discs (horizontal, vertical, or diagonal) wins!",
                "Controls: R = restart   |   ESC = back to menu",
            ]
            for i, line in enumerate(instructions):
                surf = self.font_small.render(line, True, INFO_COLOR)
                self.screen.blit(
                    surf,
                    (WINDOW_WIDTH // 2 - surf.get_width() // 2,
                     how_to_y + 35 + i * 24)
                )

            # --- Footer (student info) ---
            footer = self.font_tiny.render(
                "Ipek Nur Ercan - 220901750 - COE017",
                True, (170, 180, 210)
            )
            self.screen.blit(
                footer,
                (WINDOW_WIDTH // 2 - footer.get_width() // 2,
                 WINDOW_HEIGHT - 28)
            )

            pygame.display.flip()
            self.clock.tick(60)

    # -----------------------------------------------------------------
    # Main loop
    # -----------------------------------------------------------------
    def run(self):
        running = True
        while running:
            if not self.show_menu():
                break

            in_game = True
            while in_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        in_game = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game()
                        elif event.key == pygame.K_ESCAPE:
                            in_game = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.handle_human_move(event.pos[0])

                # AI turn
                if self.current_player == PLAYER_2 and not self.game_over:
                    self.handle_ai_move()

                self.render()
                self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    Connect4GUI().run()
