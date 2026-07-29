"""
Connect 4 AI - Main Entry Point
-------------------------------
Launch menu that lets the user choose between:
    1. Play GUI version (recommended)
    2. Play terminal version
    3. Watch AI vs AI demo
    4. Run Minimax vs Alpha-Beta benchmark

Run:
    python main.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    print("=" * 60)
    print("  CONNECT 4 - AI with Minimax & Alpha-Beta Pruning")
    print("  Course: COE017 - Principles of Artificial Intelligence")
    print("  Student: Ipek Nur Ercan - 220901750")
    print("=" * 60)
    print()
    print("Select mode:")
    print("  1) Play GUI (Pygame) - recommended")
    print("  2) Play in terminal")
    print("  3) Watch AI vs AI demo (depth 2 vs depth 5)")
    print("  4) Run Minimax vs Alpha-Beta benchmark")
    print("  5) Quit")
    print()

    choice = input("Your choice (1-5): ").strip()

    if choice == "1":
        from gui import Connect4GUI
        Connect4GUI().run()
    elif choice == "2":
        from terminal_game import human_vs_ai
        print("\nDifficulty options: easy / medium / hard")
        diff = input("Choose difficulty (default medium): ").strip() or "medium"
        human_vs_ai(diff)
    elif choice == "3":
        from terminal_game import ai_vs_ai
        ai_vs_ai(depth_x=2, depth_o=5)
    elif choice == "4":
        from benchmark import run_benchmark
        run_benchmark(max_depth=5)
    elif choice == "5":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice.")
        main()


if __name__ == "__main__":
    main()
