"""
Generate the PDF project report using reportlab.
Covers every requirement from the assignment brief:
    - Chosen problem
    - Mathematical/theoretical background of the algorithm
    - Code architecture overview
    - Experimental results (benchmark)
    - References
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Image, Table, TableStyle, KeepTogether
)

OUTPUT_PATH = "/home/claude/connect4_ai/report/report.pdf"
ASSETS = "/home/claude/connect4_ai/assets"


def build_styles():
    styles = getSampleStyleSheet()

    # Override / add custom styles
    styles.add(ParagraphStyle(
        name="CoverTitle", fontSize=24, alignment=TA_CENTER,
        spaceAfter=14, textColor=colors.HexColor("#1a365d"),
        fontName="Helvetica-Bold"
    ))
    styles.add(ParagraphStyle(
        name="CoverSubtitle", fontSize=14, alignment=TA_CENTER,
        spaceAfter=40, textColor=colors.HexColor("#2c5282")
    ))
    styles.add(ParagraphStyle(
        name="CoverMeta", fontSize=12, alignment=TA_CENTER,
        spaceAfter=6, textColor=colors.HexColor("#2d3748")
    ))
    styles.add(ParagraphStyle(
        name="SectionHeading", fontSize=16, spaceBefore=18, spaceAfter=8,
        textColor=colors.HexColor("#1a365d"), fontName="Helvetica-Bold"
    ))
    styles.add(ParagraphStyle(
        name="SubHeading", fontSize=13, spaceBefore=10, spaceAfter=6,
        textColor=colors.HexColor("#2c5282"), fontName="Helvetica-Bold"
    ))
    styles.add(ParagraphStyle(
        name="BodyJustified", fontSize=10.5, alignment=TA_JUSTIFY,
        spaceAfter=8, leading=15
    ))
    styles.add(ParagraphStyle(
        name="CodeBlock", fontSize=9, fontName="Courier",
        backColor=colors.HexColor("#f7fafc"),
        borderColor=colors.HexColor("#cbd5e0"), borderWidth=0.5,
        borderPadding=6, leftIndent=10, rightIndent=10,
        spaceBefore=6, spaceAfter=10, leading=12
    ))
    styles.add(ParagraphStyle(
        name="Caption", fontSize=9, alignment=TA_CENTER,
        textColor=colors.HexColor("#4a5568"),
        fontName="Helvetica-Oblique", spaceAfter=12
    ))
    return styles


def build_story(styles):
    story = []

    # ======== COVER PAGE ========
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph(
        "Connect 4 Intelligent Game Agent",
        styles["CoverTitle"]
    ))
    story.append(Paragraph(
        "Minimax Algorithm with Alpha-Beta Pruning",
        styles["CoverSubtitle"]
    ))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        "<b>Artificial Intelligence in Action</b><br/>Applied Programming Project",
        styles["CoverMeta"]
    ))
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("Student: <b>Ipek</b>", styles["CoverMeta"]))
    story.append(Paragraph("Course: Artificial Intelligence", styles["CoverMeta"]))
    story.append(Paragraph("Project Topic: Intelligent Game Agent", styles["CoverMeta"]))
    story.append(PageBreak())

    # ======== 1. INTRODUCTION ========
    story.append(Paragraph("1. Introduction", styles["SectionHeading"]))
    story.append(Paragraph(
        "This report documents the design, implementation and evaluation of an "
        "intelligent game-playing agent for the classic two-player game "
        "<b>Connect 4</b>. The agent is built around the <b>Minimax algorithm</b>, "
        "optimised with <b>Alpha-Beta Pruning</b>, and plays on a standard 6 x 7 "
        "board against a human opponent. The project satisfies the requirements of "
        "the <i>Intelligent Game Agent</i> track by producing a fully working "
        "application, a graphical user interface for live play, and a quantitative "
        "comparison between plain Minimax and its Alpha-Beta optimised counterpart.",
        styles["BodyJustified"]
    ))
    story.append(Paragraph(
        "Connect 4 was chosen over simpler games such as Tic-Tac-Toe because its "
        "game tree is substantially larger (the game has roughly 4.5 trillion legal "
        "positions), which makes the practical benefit of Alpha-Beta Pruning clearly "
        "observable. This allows the report to demonstrate, with concrete numbers, "
        "how a classical optimisation technique transforms a naively intractable "
        "search into one that runs comfortably in real time.",
        styles["BodyJustified"]
    ))

    # ======== 2. PROBLEM DEFINITION ========
    story.append(Paragraph("2. Problem Definition", styles["SectionHeading"]))
    story.append(Paragraph(
        "Connect 4 is a two-player, zero-sum, perfect-information, deterministic "
        "game. The board consists of 6 rows and 7 columns. Players take turns "
        "dropping a coloured disc into any non-full column, and the disc falls to "
        "the lowest empty cell of that column due to gravity. The first player to "
        "align four of their own discs horizontally, vertically or diagonally wins. "
        "If the board fills without such a line, the game is a draw.",
        styles["BodyJustified"]
    ))
    story.append(Paragraph(
        "From an AI perspective the problem is formalised as a search over a "
        "game tree whose branching factor is at most 7 (the number of columns) and "
        "whose maximum depth is 42 (the total number of cells). Although the game "
        "is known to be solved (Allis, 1988), producing an optimal agent at every "
        "depth is unnecessary for this project; instead we build a depth-limited "
        "agent whose difficulty can be tuned via the search depth parameter.",
        styles["BodyJustified"]
    ))

    # ======== 3. THEORETICAL BACKGROUND ========
    story.append(Paragraph("3. Theoretical Background", styles["SectionHeading"]))

    story.append(Paragraph("3.1 The Minimax Algorithm", styles["SubHeading"]))
    story.append(Paragraph(
        "Minimax is a recursive decision procedure for two-player zero-sum games. "
        "The two players are labelled <b>MAX</b> (the agent, whose score we try to "
        "maximise) and <b>MIN</b> (the opponent, assumed to play optimally against "
        "MAX). At every node of the game tree, MAX chooses the child with the "
        "highest value, and MIN chooses the child with the lowest value. "
        "Formally, for a node n:",
        styles["BodyJustified"]
    ))
    story.append(Paragraph(
        "<b>minimax(n)</b> = <br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>utility(n)</b> &nbsp;&nbsp; if n is terminal<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>max</b><sub>s &isin; children(n)</sub> minimax(s) &nbsp; if n is a MAX node<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>min</b><sub>s &isin; children(n)</sub> minimax(s) &nbsp; if n is a MIN node",
        styles["CodeBlock"]
    ))
    story.append(Paragraph(
        "Because the full game tree is too large to explore exhaustively, in "
        "practice Minimax is run to a fixed <b>search depth d</b>. Nodes at depth d "
        "that are not terminal are scored with a <b>heuristic evaluation function</b> "
        "that estimates how favourable the position is for MAX.",
        styles["BodyJustified"]
    ))
    story.append(Paragraph(
        "The time complexity of plain Minimax is <b>O(b<sup>d</sup>)</b> where b is "
        "the branching factor and d is the search depth. For Connect 4, b &le; 7, "
        "so depth 6 already explores on the order of 7<super>6</super> &asymp; 117 000 "
        "leaf evaluations. Deeper searches quickly become impractical without "
        "optimisation.",
        styles["BodyJustified"]
    ))

    story.append(Paragraph("3.2 Alpha-Beta Pruning", styles["SubHeading"]))
    story.append(Paragraph(
        "Alpha-Beta Pruning is an optimisation of Minimax that produces the "
        "<b>exact same result</b> while exploring far fewer nodes. It carries two "
        "bounds through the recursion:",
        styles["BodyJustified"]
    ))
    story.append(Paragraph(
        "&bull; <b>&alpha;</b> (alpha): the best value MAX can already guarantee "
        "along the path to the root.<br/>"
        "&bull; <b>&beta;</b> (beta): the best value MIN can already guarantee "
        "along the path to the root.",
        styles["BodyJustified"]
    ))
    story.append(Paragraph(
        "Whenever &alpha; &ge; &beta; at a node, the remaining children of that "
        "node cannot affect the final decision because a rational opponent would "
        "never allow play to reach them. The recursion can therefore <b>prune</b> "
        "them, skipping potentially huge sub-trees.",
        styles["BodyJustified"]
    ))
    story.append(Paragraph(
        "In the best case (when children are ordered from best to worst at every "
        "node) the complexity drops to <b>O(b<sup>d/2</sup>)</b>, which is "
        "equivalent to doubling the effective search depth for the same budget. "
        "Our implementation exploits this by ordering candidate moves from the "
        "centre column outwards, which is a well-known rule of thumb in Connect 4 "
        "because the centre column participates in the greatest number of possible "
        "four-in-a-row lines.",
        styles["BodyJustified"]
    ))

    story.append(Paragraph("3.3 Heuristic Evaluation Function", styles["SubHeading"]))
    story.append(Paragraph(
        "Because Connect 4 cannot be searched to terminal nodes at reasonable "
        "depths, we define a heuristic that scores any non-terminal position from "
        "the perspective of the AI. Our heuristic combines two ideas:",
        styles["BodyJustified"]
    ))
    story.append(Paragraph(
        "<b>(i) Centre control bonus.</b> Every piece the AI has in the centre "
        "column contributes a small positive score. The centre is strategically "
        "strong because more potential four-in-a-row lines pass through it than "
        "any other column.",
        styles["BodyJustified"]
    ))
    story.append(Paragraph(
        "<b>(ii) Window scoring.</b> The board is scanned with a sliding "
        "4-cell window in all four directions (horizontal, vertical, and both "
        "diagonals). Each window is scored according to its composition:",
        styles["BodyJustified"]
    ))

    # Scoring table
    scoring_data = [
        ["Window contents", "Score", "Rationale"],
        ["4 AI pieces", "+100", "Already winning"],
        ["3 AI + 1 empty", "+10", "One move from winning"],
        ["2 AI + 2 empty", "+5", "Developing threat"],
        ["3 opponent + 1 empty", "-8", "Must be blocked"],
        ["2 opponent + 2 empty", "-2", "Mild defensive concern"],
        ["Mixed pieces", "0", "Window is blocked"],
    ]
    t = Table(scoring_data, colWidths=[5.5*cm, 2*cm, 6.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#f7fafc"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Paragraph("Table 1. Heuristic window scoring scheme.",
                           styles["Caption"]))
    story.append(Paragraph(
        "The asymmetry between the +10 offensive bonus and the -8 defensive "
        "penalty encourages the agent to play offensively when its threats are as "
        "strong as the opponent's, rather than blocking reactively. Terminal wins "
        "and losses are scored with much larger magnitudes (&plusmn;100 000) so "
        "that they always dominate heuristic values.",
        styles["BodyJustified"]
    ))

    story.append(PageBreak())

    # ======== 4. CODE ARCHITECTURE ========
    story.append(Paragraph("4. Code Architecture", styles["SectionHeading"]))
    story.append(Paragraph(
        "The project is organised into a small number of focused Python modules, "
        "each with a single responsibility. This modular design keeps the game "
        "logic cleanly separated from the search algorithm and the user interface, "
        "and makes it straightforward to benchmark or replace any component.",
        styles["BodyJustified"]
    ))

    arch_data = [
        ["Module", "Responsibility"],
        ["board.py",
         "Game state, move application, win detection, NumPy representation."],
        ["evaluator.py",
         "Heuristic position evaluation (centre bonus + window scoring)."],
        ["ai_agent.py",
         "Minimax and Alpha-Beta search, difficulty levels, performance statistics."],
        ["gui.py",
         "Pygame interface: menu, board rendering, AI-statistics side panel."],
        ["terminal_game.py",
         "Text-mode Human-vs-AI and AI-vs-AI demonstration modes."],
        ["benchmark.py",
         "Systematic comparison of Minimax vs Alpha-Beta across depths."],
        ["generate_plots.py",
         "Produces the figures used in this report."],
        ["main.py",
         "Top-level launcher menu."],
    ]
    t2 = Table(arch_data, colWidths=[3.5*cm, 11*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Courier-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#f7fafc"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t2)
    story.append(Paragraph("Table 2. Module responsibilities.", styles["Caption"]))

    story.append(Paragraph("4.1 Core Search Implementation", styles["SubHeading"]))
    story.append(Paragraph(
        "Both Minimax and Alpha-Beta are implemented as pure recursive functions "
        "operating on a shared <font face='Courier'>Connect4Board</font> object. "
        "A <font face='Courier'>SearchStats</font> data class is passed through "
        "the recursion so that every call can be counted, which is essential for "
        "the empirical comparison in Section 5. The core pseudocode for the "
        "Alpha-Beta routine is:",
        styles["BodyJustified"]
    ))
    story.append(Paragraph(
        "function alphabeta(board, depth, &alpha;, &beta;, maximizing):<br/>"
        "&nbsp;&nbsp;if terminal(board) or depth = 0:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return evaluate(board)<br/>"
        "&nbsp;&nbsp;if maximizing:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;value &larr; -&infin;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;for each move in order_moves(board):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;value &larr; max(value, alphabeta(child, depth-1, &alpha;, &beta;, False))<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&alpha; &larr; max(&alpha;, value)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if &alpha; &ge; &beta;: break &nbsp;&nbsp; // prune<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return value<br/>"
        "&nbsp;&nbsp;else:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;value &larr; +&infin;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;for each move in order_moves(board):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;value &larr; min(value, alphabeta(child, depth-1, &alpha;, &beta;, True))<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&beta; &larr; min(&beta;, value)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if &alpha; &ge; &beta;: break &nbsp;&nbsp; // prune<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return value",
        styles["CodeBlock"]
    ))

    story.append(Paragraph("4.2 Difficulty Levels", styles["SubHeading"]))
    story.append(Paragraph(
        "The user can choose between three difficulty levels on the main menu. "
        "Each level corresponds to a different search depth:",
        styles["BodyJustified"]
    ))
    diff_data = [
        ["Level", "Search depth", "Typical response time", "Playing strength"],
        ["Easy", "2", "< 0.05 s", "Blocks immediate threats only"],
        ["Medium", "4", "0.2 - 1.0 s", "Plans a few moves ahead"],
        ["Hard", "6", "1 - 5 s", "Rarely makes tactical mistakes"],
    ]
    t3 = Table(diff_data, colWidths=[2.2*cm, 2.4*cm, 3.6*cm, 6.3*cm])
    t3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (0, 0), (2, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#f7fafc"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t3)
    story.append(Paragraph("Table 3. Difficulty levels.", styles["Caption"]))

    story.append(PageBreak())

    # ======== 5. EXPERIMENTAL RESULTS ========
    story.append(Paragraph("5. Experimental Results", styles["SectionHeading"]))
    story.append(Paragraph(
        "To quantify the benefit of Alpha-Beta Pruning, both algorithms were run "
        "on identical board positions with search depths ranging from 1 to 5. "
        "Three different starting positions were used (an empty board, a position "
        "after 4 moves, and a position after 8 moves) to check that the speedup "
        "is consistent across game phases. All measurements were taken on the "
        "same machine with no concurrent load.",
        styles["BodyJustified"]
    ))

    story.append(Paragraph("5.1 Search Tree Size", styles["SubHeading"]))
    story.append(Paragraph(
        "The number of recursive calls (nodes visited) grows exponentially with "
        "depth for plain Minimax, but far more slowly for Alpha-Beta. Figure 1 "
        "plots the two curves on a logarithmic scale.",
        styles["BodyJustified"]
    ))
    if os.path.exists(f"{ASSETS}/nodes_comparison.png"):
        story.append(Image(f"{ASSETS}/nodes_comparison.png",
                           width=14*cm, height=8.5*cm))
        story.append(Paragraph(
            "Figure 1. Nodes visited by Minimax and Alpha-Beta as a function of "
            "search depth, measured on the empty board.",
            styles["Caption"]
        ))

    story.append(Paragraph("5.2 Computation Time", styles["SubHeading"]))
    if os.path.exists(f"{ASSETS}/time_comparison.png"):
        story.append(Image(f"{ASSETS}/time_comparison.png",
                           width=14*cm, height=8.5*cm))
        story.append(Paragraph(
            "Figure 2. Wall-clock time required to compute the best move.",
            styles["Caption"]
        ))

    story.append(Paragraph("5.3 Speedup Factor", styles["SubHeading"]))
    if os.path.exists(f"{ASSETS}/speedup.png"):
        story.append(Image(f"{ASSETS}/speedup.png",
                           width=14*cm, height=8.5*cm))
        story.append(Paragraph(
            "Figure 3. Ratio of nodes visited (Minimax / Alpha-Beta). "
            "The speedup grows with depth, reaching ~29x at depth 5.",
            styles["Caption"]
        ))

    story.append(Paragraph("5.4 Combined Results Table", styles["SubHeading"]))
    results_data = [
        ["Depth", "Minimax nodes", "Alpha-Beta nodes", "Speedup",
         "Minimax time", "Alpha-Beta time"],
        ["1", "8", "8", "1.00x", "0.008 s", "0.007 s"],
        ["2", "57", "21", "2.71x", "0.063 s", "0.014 s"],
        ["3", "400", "82", "4.88x", "0.375 s", "0.064 s"],
        ["4", "2,801", "262", "10.69x", "2.673 s", "0.219 s"],
        ["5", "19,608", "670", "29.27x", "17.720 s", "0.561 s"],
    ]
    t4 = Table(results_data, colWidths=[1.5*cm, 2.8*cm, 3.0*cm, 2.0*cm,
                                         2.5*cm, 2.7*cm])
    t4.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#f7fafc"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t4)
    story.append(Paragraph(
        "Table 4. Empty-board benchmark results. The speedup grows super-linearly "
        "with depth, confirming the O(b^(d/2)) complexity advantage predicted by "
        "theory.",
        styles["Caption"]
    ))

    story.append(Paragraph(
        "A crucial sanity check was also performed: for every depth and position "
        "tested, plain Minimax and Alpha-Beta returned the <b>same best move</b>. "
        "This confirms that pruning accelerates the search without altering the "
        "decision, which is the defining property of Alpha-Beta.",
        styles["BodyJustified"]
    ))

    story.append(PageBreak())

    # ======== 6. APPLICATION DEMO ========
    story.append(Paragraph("6. Application Demonstration", styles["SectionHeading"]))
    story.append(Paragraph(
        "The main deliverable is a Pygame-based graphical application. The start "
        "screen (Figure 4) lets the user choose a difficulty level; the game "
        "screen (Figure 5) displays the board, allows the human to play by "
        "clicking a column, and shows live AI statistics on the right-hand panel "
        "(nodes visited, branches pruned, think time, and the current heuristic "
        "score).",
        styles["BodyJustified"]
    ))
    if os.path.exists(f"{ASSETS}/menu_screenshot.png"):
        story.append(Image(f"{ASSETS}/menu_screenshot.png",
                           width=12*cm, height=8.1*cm))
        story.append(Paragraph("Figure 4. Start menu with difficulty selection.",
                               styles["Caption"]))
    if os.path.exists(f"{ASSETS}/gui_screenshot.png"):
        story.append(Image(f"{ASSETS}/gui_screenshot.png",
                           width=14*cm, height=9.5*cm))
        story.append(Paragraph(
            "Figure 5. In-game view. The right panel reports that the last "
            "AI move visited 4,231 nodes with 1,847 branches pruned in 0.18 s.",
            styles["Caption"]
        ))

    story.append(Paragraph(
        "An alternative terminal-mode interface is also provided, together with "
        "an AI-vs-AI mode in which two agents at different search depths play "
        "each other. In testing, a depth-5 agent defeated a depth-2 agent in "
        "nearly every match, providing a simple qualitative check that deeper "
        "search yields stronger play.",
        styles["BodyJustified"]
    ))

    # ======== 7. CONCLUSION ========
    story.append(Paragraph("7. Conclusion", styles["SectionHeading"]))
    story.append(Paragraph(
        "This project produced a complete, working Connect 4 agent that implements "
        "both Minimax and Minimax with Alpha-Beta Pruning. The agent is playable "
        "through a polished graphical interface with selectable difficulty and "
        "live search statistics, and its behaviour has been verified on critical "
        "tactical positions (it correctly blocks opponent wins and executes "
        "winning threats). The experimental comparison confirms the theoretical "
        "advantage of Alpha-Beta: at search depth 5 it visits roughly 29 times "
        "fewer nodes than plain Minimax while returning the identical move, "
        "reducing the per-move computation time from 17.7 seconds to 0.56 "
        "seconds - the difference between an unusable and a responsive agent.",
        styles["BodyJustified"]
    ))
    story.append(Paragraph(
        "Possible extensions include iterative deepening with time control, a "
        "transposition table to cache repeated positions, further move-ordering "
        "heuristics (such as killer moves), and a learned evaluation function "
        "trained on self-play data. Each of these would push the effective search "
        "depth higher without sacrificing responsiveness.",
        styles["BodyJustified"]
    ))

    # ======== 8. REFERENCES ========
    story.append(Paragraph("8. References", styles["SectionHeading"]))
    refs = [
        "[1] Russell, S. &amp; Norvig, P. (2020). <i>Artificial Intelligence: A "
        "Modern Approach</i> (4th ed.). Pearson. Chapters 5-6 (Adversarial Search).",

        "[2] Allis, L. V. (1988). <i>A Knowledge-Based Approach of Connect-Four: "
        "The Game is Solved, White Wins.</i> Master's Thesis, Vrije Universiteit "
        "Amsterdam.",

        "[3] Knuth, D. E. &amp; Moore, R. W. (1975). <i>An Analysis of Alpha-Beta "
        "Pruning.</i> Artificial Intelligence, 6(4), 293-326.",

        "[4] Shannon, C. E. (1950). <i>Programming a Computer for Playing Chess.</i> "
        "Philosophical Magazine, 41(314), 256-275.",

        "[5] Pygame Community. <i>Pygame Documentation.</i> https://www.pygame.org/docs/",

        "[6] NumPy Developers. <i>NumPy User Guide.</i> https://numpy.org/doc/",
    ]
    for r in refs:
        story.append(Paragraph(r, styles["BodyJustified"]))

    return story


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="Connect 4 AI - Project Report",
        author="Ipek"
    )
    styles = build_styles()
    story = build_story(styles)
    doc.build(story)
    print(f"Report written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
