# Connect 4 Intelligent Game Agent

**Course:** Artificial Intelligence — Applied Programming Project
**Student:** Ipek
**Topic:** Intelligent Game Agent (Minimax + Alpha-Beta Pruning)

A Connect 4 game with an AI opponent that plays using the Minimax algorithm, optimised with Alpha-Beta Pruning. Built in Python with Pygame.

---

## Features

- **Graphical interface** (Pygame) with click-to-drop controls
- **Three difficulty levels**: Easy (depth 2), Medium (depth 4), Hard (depth 6)
- **Live AI statistics panel** showing nodes visited, branches pruned, think time
- **Terminal mode** for environments without a display
- **AI-vs-AI demo** where two agents at different depths play each other
- **Benchmark suite** comparing plain Minimax against Alpha-Beta Pruning
- **Winning line highlight** and game restart with the R key

---

## Requirements

- Python 3.9 or newer
- Install dependencies with:
  ```bash
  pip install -r requirements.txt
  ```

The dependencies are:
- `pygame` — graphical interface
- `numpy` — fast board representation
- `matplotlib` — benchmark plots
- `reportlab` — PDF report generation

---

## How to Run

From the project root:

```bash
python src/main.py
```

This opens a menu with five options:

| Option | Description |
|--------|-------------|
| 1 | Play the graphical Pygame version (recommended) |
| 2 | Play in terminal mode |
| 3 | Watch an AI-vs-AI demo (depth 2 vs depth 5) |
| 4 | Run the Minimax vs Alpha-Beta benchmark |
| 5 | Quit |

You can also run any component directly:

```bash
python src/gui.py              # graphical game only
python src/terminal_game.py    # terminal game only
python src/benchmark.py        # benchmark only
```

### In-game controls (GUI)

- **Left click** on a column to drop your piece
- **R** to restart the current game
- **ESC** to return to the main menu

---

## Project Structure

```
connect4_ai/
├── src/
│   ├── board.py            # Game state and rules
│   ├── evaluator.py        # Heuristic evaluation function
│   ├── ai_agent.py         # Minimax and Alpha-Beta search
│   ├── gui.py              # Pygame graphical interface
│   ├── terminal_game.py    # Terminal-mode gameplay
│   ├── benchmark.py        # Minimax vs Alpha-Beta comparison
│   ├── generate_plots.py   # Plots used in the report
│   ├── generate_report.py  # Builds the PDF report
│   └── main.py             # Launcher menu
├── assets/                 # Screenshots and plots
├── report/
│   └── report.pdf          # Full project report
├── requirements.txt
└── README.md
```


## Algorithms Implemented

- **Minimax** (unoptimised, for benchmarking only)
- **Minimax + Alpha-Beta Pruning** (production algorithm)
- **Heuristic evaluation** combining centre-column bonus with sliding-window scoring in all four directions
- **Move ordering** (centre-outward) to maximise Alpha-Beta's pruning effectiveness

