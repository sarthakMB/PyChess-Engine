# Welcome to PyChess Engine

A simple but fast chess engine made in Python.

## Features

- **Chess Engine** - Complete chess logic implementation in Python
- **Web Frontend** - Modern, responsive UI built with chessboard.js and Tailwind CSS
- **REST API Ready** - Frontend designed for server-side game logic

## Project Structure

- `board.py` - Core chess engine implementation
- `frontend/` - Web-based chess interface
- `test.py` - Test suite
- `CLAUDE.md` - Developer documentation

## Getting Started

### Chess Engine
```python
from board import Board, Position

# Create a new game
board = Board()

# Make a move
old_pos = Position(6, 4)  # e2
new_pos = Position(4, 4)  # e4
board.move_piece(old_pos, new_pos)
```

### Frontend
See `frontend/README.md` for details.

Open `frontend/index.html` in a browser or run a local server:
```bash
cd frontend
python -m http.server 8000
```

Then visit `http://localhost:8000`
