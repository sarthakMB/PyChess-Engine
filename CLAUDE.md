# CLAUDE.md - PyChess Engine

## Project Overview

PyChess Engine is a simple but fast chess engine implemented in Python. The project focuses on chess move generation, validation, and basic game state management without external dependencies.

**Project Status**: Active development with core chess logic implemented. Some advanced features (castling, en passant, FEN updates) are pending implementation.

## Repository Structure

```
PyChess-Engine/
├── board.py         # Core chess engine (26KB) - All game logic
├── test.py          # Simple test file
├── log.py           # Empty logging file (placeholder)
├── output.txt       # Game move history output (6.8MB)
└── README.md        # Project description
```

## Code Architecture

### Core Components

#### 1. Board Class (`board.py:4-314`)

The main class managing the chess board state, moves, and game rules.

**Key Attributes:**
- `board`: 8x8 2D list representing the chess board
- `fen`: FEN notation string for board position
- `white_to_play`: Boolean indicating current player
- `piece_list`: List of all piece objects
- `position_list`: List tracking piece positions
- `game_history_state`: Stack of board states for undo/redo
- `game_history_fen`: Stack of FEN positions
- Castle rights: `white_king_side_castle`, `white_queen_side_castle`, etc.
- `en_passant`: Current en passant target square
- `halfmove_number`, `fullmove_number`: Move counters

**Key Methods:**

**Move Handling:**
- `move_piece(old_position, new_position)` (`board.py:62`) - Executes a move with validation
- `_is_move_valid(old_position, new_position)` (`board.py:146`) - Validates if a move is legal
- `_valid_moves(position)` (`board.py:157`) - Returns all legal moves for a piece
- `_king_checked_after_move(old_position, new_position)` (`board.py:169`) - Checks if move leaves king in check

**Game State:**
- `is_check()` (`board.py:285`) - Detects if current player is in check
- `is_mate()` (`board.py:276`) - Detects if current player has no legal moves
- `is_checkmate()` (`board.py:300`) - Checks for checkmate condition
- `_save_state()` (`board.py:104`) - Saves current board state to history
- `_restore_state(state)` (`board.py:119`) - Restores a saved board state
- `_restore_history_last()` (`board.py:134`) - Undo last move
- `_restore_history_next()` (`board.py:140`) - Redo next move

**Board Management:**
- `_construct_board(fen)` (`board.py:211`) - Builds board from FEN notation
- `_board_vs_piece_list_check()` (`board.py:303`) - Validates board consistency
- `_play_random_move()` (`board.py:247`) - Plays a random legal move (for testing)

**Incomplete Methods (stubs):**
- `_update_fen()` (`board.py:238`) - TODO: Update FEN string after moves
- `_check_castling()` (`board.py:241`) - TODO: Handle castling logic
- `_check_en_passant()` (`board.py:244`) - TODO: Handle en passant logic

#### 2. Position Class (`board.py:317-329`)

Represents board coordinates.

**Attributes:**
- `row`: 0-7, where 0 = black's back rank, 7 = white's back rank
- `col`: 0-7, where 0 = 'a' file, 7 = 'h' file

**Special Positions:**
- `Position(-1, -1)`: Indicates a captured piece

#### 3. Piece Classes (`board.py:331-491`)

**Base Class: Piece** (`board.py:331`)
- `is_white`: Boolean for piece color
- `position`: Position object

**Derived Classes:**
- `Pawn` (`board.py:336`) - Implements pawn movement and captures
- `Rook` (`board.py:376`) - Implements rook movement (straight lines)
- `Knight` (`board.py:401`) - Implements knight movement (L-shape)
- `Bishop` (`board.py:422`) - Implements bishop movement (diagonals)
- `Queen` (`board.py:447`) - Implements queen movement (rook + bishop)
- `King` (`board.py:472`) - Implements king movement (one square any direction)

**Key Method:**
- `possible_moves(board)`: Returns list of possible moves without checking for checks

## Development Guidelines

### Working with the Codebase

#### Adding New Features

1. **Implement missing features** in this order:
   - `_update_fen()` - Critical for proper FEN notation support
   - `_check_castling()` - Implement castling rules
   - `_check_en_passant()` - Implement en passant captures

2. **Extending piece logic:**
   - Add new methods to piece classes
   - Update `_valid_moves()` if special rules apply
   - Maintain consistency with existing movement patterns

3. **Adding game features:**
   - Update Board class state variables
   - Add to `_save_state()` and `_restore_state()` for undo/redo support
   - Consider FEN notation implications

#### Code Conventions

**Naming:**
- Public methods: `method_name()`
- Private methods: `_method_name()`
- Classes: `PascalCase`
- Variables: `snake_case`

**Piece Representation:**
- White pieces: Uppercase letters (P, R, N, B, Q, K)
- Black pieces: Lowercase letters (p, r, n, b, q, k)
- Empty square: Single space `" "`

**Board Coordinates:**
- Row 0 = Black's back rank (8th rank in chess notation)
- Row 7 = White's back rank (1st rank in chess notation)
- Col 0 = 'a' file
- Col 7 = 'h' file

**State Management:**
- Always use assertions to validate board consistency
- Call `_save_state()` after moves
- Use `_board_vs_piece_list_check()` to verify consistency

### Testing

**Current Test Infrastructure:**
- `test.py` - Basic test skeleton
- `main()` function in `board.py` (`board.py:493`) - Plays random games until mate

**Running Tests:**
```bash
python board.py    # Runs random game simulation
python test.py     # Runs basic tests
```

**Test Output:**
- Game moves written to `output.txt`
- Console shows board state after each move

**Adding Tests:**
1. Add test methods to `test.py`
2. Test edge cases: check, checkmate, stalemate
3. Validate FEN parsing with known positions
4. Test piece movement for all piece types
5. Verify undo/redo functionality

### Debugging

**Common Debugging Points:**
- Check assertions throughout `_play_random_move()` (`board.py:247-274`)
- Use `_board_vs_piece_list_check()` to verify board consistency
- Verify position updates when moving pieces
- Check that killed pieces have `Position(-1, -1)`

**Debugging Tools:**
- `print(board)` - Display current board state
- `board.__str__()` - Returns formatted board string with captured pieces
- Assertions are extensively used for validation

## Known Issues and TODOs

### Critical Missing Features

1. **FEN Update** (`board.py:238`)
   - `_update_fen()` is not implemented
   - FEN string doesn't update after moves
   - Impacts: Game state export, position sharing

2. **Castling** (`board.py:241`)
   - `_check_castling()` is a stub
   - Castle rights tracked but not enforced
   - Needs: King/rook movement detection, path validation

3. **En Passant** (`board.py:244`)
   - `_check_en_passant()` is a stub
   - Variable exists but not used in move validation
   - Needs: Pawn double-move detection, en passant capture logic

### Potential Improvements

1. **Pawn Promotion**
   - Not implemented (see `board.py:345` - returns empty if row 0 or 7)
   - Should handle promotion when pawn reaches back rank

2. **Stalemate Detection**
   - `is_mate()` detects no moves, but doesn't distinguish stalemate
   - Need separate stalemate check (no legal moves + not in check)

3. **Threefold Repetition / Fifty-Move Rule**
   - Draw conditions not implemented
   - Could use `game_history_fen` for repetition detection

4. **Move Notation**
   - No algebraic notation support
   - Position uses (row, col) instead of chess notation

5. **Performance**
   - Consider optimizing `_king_checked_after_move()` (makes/unmakes moves)
   - Could use attack tables or bitboards for speed

## Working with Move Validation

### Move Validation Flow

```
User calls move_piece(old_pos, new_pos)
  ↓
_is_move_valid() checks if move in _valid_moves()
  ↓
_valid_moves() gets piece.possible_moves() filtered by _king_checked_after_move()
  ↓
_king_checked_after_move() temporarily makes move and checks if king under attack
  ↓
If valid: execute move, update state, save history
```

### Important Invariants

1. **Board-Piece List Consistency:**
   - Every piece in `piece_list` with `position != (-1, -1)` must be on board
   - Every piece on board must be in `piece_list`
   - Verified by `_board_vs_piece_list_check()`

2. **Position Synchronization:**
   - Piece object's `position` attribute must match board location
   - Killed pieces must have `position = Position(-1, -1)`

3. **State History:**
   - `game_history_state` length should match halfmove progression
   - Assert at `board.py:115`: `len(self.game_history_state) >= self.halfmove_number`

## Extending the Engine

### Adding a New Piece Type

1. Create new class inheriting from `Piece`
2. Implement `possible_moves(board)` method
3. Add parsing in `_construct_board()` for FEN character
4. Add `__str__()` method returning piece symbol

### Adding Move Notation Support

1. Create position parsing: "e4" → Position(4, 4)
2. Implement move notation: "Nf3", "O-O", etc.
3. Update `move_piece()` to accept notation strings
4. Add method to export moves in PGN format

### Adding Engine Evaluation

1. Add piece value constants (P=1, N=3, B=3, R=5, Q=9)
2. Implement `evaluate_position()` method
3. Add minimax or alpha-beta search
4. Replace `_play_random_move()` with `_play_best_move()`

## Git Workflow

**Current Branch:** `claude/claude-md-mi0e9k6dpe8bx5gi-01FnbMQbELT96VcNMJgAMZFW`

**Recent Commits:**
- `a2a5418` - "fixed bugs added asserts"
- `97823fb` - "batman"

**Best Practices:**
- Commit after implementing each complete feature
- Use descriptive commit messages
- Test before committing (run `board.py` to verify no crashes)
- Keep commits focused on single features

## Quick Reference

### Creating a Board
```python
from board import Board, Position

# Default starting position
board = Board()

# From FEN
board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
```

### Making Moves
```python
# Move a piece
old_pos = Position(6, 4)  # White pawn on e2
new_pos = Position(4, 4)  # Move to e4
kill, killed_piece, killed_pos = board.move_piece(old_pos, new_pos)
```

### Checking Game State
```python
if board.is_check():
    print("King in check!")

if board.is_checkmate():
    print("Checkmate!")

if board.is_mate() and not board.is_check():
    print("Stalemate!")
```

### Getting Valid Moves
```python
position = Position(6, 4)  # White pawn on e2
valid_moves = board._valid_moves(position)
for move in valid_moves:
    print(f"Can move to ({move.row}, {move.col})")
```

## AI Assistant Guidelines

When working on this codebase:

1. **Always validate board consistency** - Use `_board_vs_piece_list_check()` assertions
2. **Maintain state history** - Update `_save_state()` when adding new state variables
3. **Test with random games** - Run `board.py` main() to ensure no crashes
4. **Respect the coordinate system** - Row 0 is black's side, Position(-1,-1) for killed pieces
5. **Follow FEN notation** - Even though `_update_fen()` is incomplete, maintain FEN compatibility
6. **Preserve assertions** - They're critical for catching bugs in game logic
7. **Don't remove debug output** - The extensive printing in `_play_random_move()` is intentional

### Common Tasks

**Implementing Missing Features:**
- Start with `_update_fen()` - it's needed for proper game state
- Then `_check_castling()` - frequently requested chess feature
- Finally `_check_en_passant()` - completes standard chess rules

**Bug Fixes:**
- Check piece position updates in `move_piece()`
- Verify `_king_checked_after_move()` properly unmakes moves
- Ensure `piece_list` and `position_list` stay synchronized

**Performance Optimization:**
- Profile `_king_checked_after_move()` first - it's called frequently
- Consider caching valid moves
- Evaluate move ordering for alpha-beta pruning preparation

---

**Last Updated:** 2025-11-15
**Repository:** PyChess-Engine
**For:** Claude and other AI assistants
