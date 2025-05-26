# 🧩 2048 Game - Python Tkinter Implementation

This is a GUI-based version of the classic **2048 game**, built using **Python 3.10** and the **tkinter** library. The project follows the **Model-View-Controller (MVC)** architecture and was developed as part of the **CSSE1001/CSSE7030** course at the University of Queensland.

---

## 🎮 Game Features

- 4x4 tile grid that supports directional movement and merging
- Tile generation (2s and occasional 4s)
- Keyboard input using `W`, `A`, `S`, `D` keys
- Win detection (when a 2048 tile is reached)
- Loss detection (when no moves are available)
- Message prompt for win/loss with "play again" option
- Modular and testable MVC design

---

## 🧱 Code Structure

The project uses MVC design for clean separation of logic and UI:

### 📦 `Model` class

Handles all game state and logic:
- `move_left`, `move_right`, `move_up`, `move_down`
- `get_tiles`, `add_tile`, `has_won`, `has_lost`
- `attempt_move(move: str) -> bool`

### 🎨 `GameGrid` (View)

Inherits from `tk.Canvas`, and:
- Displays tiles with color-coded rectangles and text
- Handles drawing and updating based on game state
- Methods: `_get_bbox`, `_get_midpoint`, `clear`, `redraw`

### 🎮 `Game` (Controller)

- Creates the GUI window
- Binds keypress events to model actions
- Displays win/loss messages
- Facilitates MVC communication
