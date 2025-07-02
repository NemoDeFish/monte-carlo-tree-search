# 🎮 Monte Carlo Tree Search Agent for Tetress

An intelligent AI agent for the board game **Tetress**, built using **Monte Carlo Tree Search (MCTS)** and bitboard optimizations.

⚠️ **Note:** The `referee` module used to run the game is not included in this repository. Users must implement their own referee interface if they wish to run the game.

---

## 🚀 Features

### 🧠 Monte Carlo Tree Search (MCTS)

Implemented in `monte_carlo_tree_search.py`, this module performs simulations to identify optimal moves:
- **Tree search with UCT**: Balances exploration and exploitation via the Upper Confidence Bound formula.
- **Simulation-based learning**: Performs playouts to estimate move value.
- **Efficient rollout + backpropagation**: Propagates results through the tree to inform future decisions.
- **Turn-depth estimation**: Tracks the deepest simulation turn for performance profiling.

### ⚡ Bitboard Representation

The game board is encoded using **two 128-bit integers** — one for each player — for rapid computation in `board.py`:
- Fast bitwise operations for placing/removing tokens.
- Compact representation improves memory efficiency and enables fast simulations.
- Includes methods to:
  - Detect terminal states.
  - Clear full rows/columns.
  - Track and display board state.
  - Convert between coordinates and bitboards.

### 🔍 Move Generation & Evaluation

- **Move Ordering**: Prioritizes moves that reduce opponent's options using a heuristic that ranks children based on how constrained the opponent becomes.
- **Random Child Selection**: Used in MCTS rollouts for simulating random play.
- **Adjacency Filtering**: Efficient move generation ensures that only valid adjacent placements are considered.

### 🗺️ Precomputed Lookup Tables

- **`lookup_table`** (from `generate_possible_moves.py`): Maps every empty position to valid tetromino placements, enabling constant-time access during search.
- **`adjacency_table`** (from `generate_adjacency.py`): Maps positions to their adjacent coordinates to ensure pieces are only placed in legally adjacent regions.

These tables are generated at runtime and cached for speed, significantly accelerating move validation and generation.

---

## 📁 Project Structure

```bash
.
│── board.py                    # Bitboard class with full game logic
│── monte_carlo_tree_search.py  # MCTS agent logic
│── generate_possible_moves.py  # Precomputes tetromino placement lookup table
│── generate_adjacency.py       # Precomputes adjacency constraints
│── lookup_table.py             # Generated from generate_possible_moves
│── adjacency_table.py          # Generated from generate_adjacency
├── README.md
````

---

## 🛠️ Installation & Usage

### Requirements

* Python 3.12
* No external libraries required beyond the standard library.

### Setup

```bash
git clone https://github.com/NemoDeFish/monte-carlo-tree-search.git
cd monte-carlo-tree-search
```

### Running the Agent

To test locally:
* Create a custom `referee.py` with a valid game loop.

A referee must:

* Call `agent.Agent.init(...)` to initialize.
* Use `agent.Agent.action(...)` to receive the agent’s move.
* Call `agent.Agent.update(...)` after every move made by either player.
