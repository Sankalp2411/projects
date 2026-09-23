# ⚔️ MindWar Arena

> **A high-performance offline strategy game engine and AI arena featuring 9 deterministic 1v1 board combat games.**

MindWar Arena combines modern graphics rendering (OpenGL 3.3+ via ModernGL and Pygame) with an intelligent, plug-and-play AI architecture featuring Minimax with Alpha-Beta pruning, iterative deepening, transposition tables, and Monte Carlo Tree Search (MCTS).

---

## 🎮 Featured Games

| Game | Board Architecture | AI Search Method | Special Rules Implemented |
|---|---|---|---|
| **Chess** | 8×8 Matrix | Alpha-Beta + Piece-Square Tables | En Passant, Castling, Pawn Promotion, 50-move rule |
| **Checkers** | 8×8 Diagonal Matrix | Alpha-Beta Minimax | Mandatory Jumps, Multi-Jump sequences, Kinging |
| **Connect Four** | 7×6 Grid | Alpha-Beta Minimax | Column drop physics, 4-in-a-row detection |
| **Othello** | 8×8 Grid | Alpha-Beta + Positional Weight Map | Flanking disk flips, Pass turns, End-game disk count |
| **Gomoku** | 15×15 Intersection Board | Heuristic Pattern Evaluation | Five-in-a-row detection, threat scoring |
| **Pente** | 19×19 Intersection Board | Pattern + Custodial Capture Scoring | 5-in-a-row, 5-pair capture victory condition |
| **Nine Men's Morris** | 24-point Planar Graph | 3-Phase State Machine | Placement, Movement, Flying, Mill formation |
| **Go** | 9×9 / 19×19 Go Board | Monte Carlo Tree Search (MCTS) | Liberties, Suicide rule, Simple Ko rule, Territory |
| **Tic-Tac-Toe** | 3×3 Grid | Exact Minimax | Unbeatable baseline agent |

---

## 🏛️ System Architecture

MindWar Arena uses a decoupled, event-driven layered architecture:

```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│   Pygame Event Pump  │  ModernGL Shaders  │  2.5D Cam  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                    Scene Management                    │
│   BootScene  │  MainMenuScene  │  ModeScene  │  Game   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                      Game Layer                        │
│          GameBase (Undo/Redo, Timers, Lifecycle)       │
│             └── 9 Concrete Game Modules                │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                   Asynchronous AI                      │
│     Non-Blocking Worker  │  Minimax  │  MCTS  │  TT     │
└────────────────────────────────────────────────────────┘
```

### Key Highlights:
- **Asynchronous AI Processing**: AI decision-making runs on a background daemon worker thread. The UI maintains a steady 60 FPS without hanging or dropping frames even on deep `IMPOSSIBLE` difficulty searches.
- **Unified GameBase**: All 9 games inherit from `engine.game_base.GameBase`, standardizing undo/redo state stacks, turn switching, and event emissions.
- **Hardware-Accelerated Rendering**: Custom GLSL vertex and fragment shaders power geometric primitives, boards, lighting, and HUD overlays.
- **Robust Event Bus**: `EventManager` allows components to loosely couple to game occurrences (`ON_MOVE_MADE`, `ON_TURN_CHANGED`, `ON_AI_THINKING_START`, `ON_GAME_OVER`).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- An OpenGL 3.3 compatible graphics card or driver

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/mindwar-arena.git
   cd mindwar-arena
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Arena
Launch the application via either launcher:
```bash
python main.py
# or
python launcher.py
```

### In-Game Controls
- **Left Click**: Select and move pieces / drop tokens
- **Ctrl + Z / U**: Undo move (automatically rolls back 2 half-moves in Human vs AI mode)
- **Ctrl + Y / R**: Redo move
- **H**: Request AI best-move hint
- **Escape**: Return to Main Menu / Exit

---

## 🧪 Testing & Quality Assurance

Run the automated test suite with pytest:
```bash
pytest tests/ -v
```

Execute the headless aggressive AI-vs-AI stress test across all 9 games:
```bash
python tests/finalize_test.py --duration 30
```

---

## 📄 License
This project is licensed under the MIT License.
