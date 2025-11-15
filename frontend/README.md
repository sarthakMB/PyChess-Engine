# PyChess Engine - Frontend

A modern, responsive chess interface built with HTML, CSS (Tailwind), and minimal JavaScript.

## Features

- **Interactive Chessboard** - Built with chessboard.js
- **Modern UI** - Gradient backgrounds, smooth animations, responsive design
- **Game Controls** - New game, flip board functionality
- **Move History** - Track all moves with visual history
- **Captured Pieces** - Display captured pieces for both sides
- **FEN Display** - Show current position in FEN notation
- **Game Status** - Real-time status updates (turn, check, checkmate)

## Project Structure

```
frontend/
├── index.html           # Main HTML file
├── css/
│   └── styles.css      # Custom CSS styles
├── js/
│   └── board.js        # Board initialization and UI logic
└── README.md           # This file
```

## Getting Started

### Option 1: Open Directly
Simply open `index.html` in a web browser:

```bash
# From the frontend directory
open index.html           # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

### Option 2: Local Web Server
For better development experience, use a local web server:

```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js (if you have http-server installed)
npx http-server -p 8000
```

Then navigate to `http://localhost:8000` in your browser.

## Technologies Used

- **chessboard.js** - Chess board UI component
- **Tailwind CSS** - Utility-first CSS framework (via CDN)
- **jQuery** - Required by chessboard.js
- **Vanilla JavaScript** - Minimal custom logic

## API Integration

The frontend is designed to work with a REST API backend. Update the `API_BASE_URL` in `js/board.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### Expected API Endpoints

The frontend expects the following API endpoints:

- `POST /api/move` - Make a move
  ```json
  Request: { "from": "e2", "to": "e4" }
  Response: { "success": true, "fen": "...", "status": "...", ... }
  ```

- `GET /api/board` - Get current board state
  ```json
  Response: { "fen": "...", "turn": "white", "status": "In Progress", ... }
  ```

- `POST /api/new-game` - Start a new game
  ```json
  Response: { "fen": "...", "success": true }
  ```

- `GET /api/valid-moves/:position` - Get valid moves for a piece
  ```json
  Response: { "moves": ["e3", "e4"] }
  ```

## Backend Integration (Coming Soon)

Two backend options are being considered:

### Option 1: Python (Flask/Django)
- Reuse existing `board.py` chess engine
- Flask for lightweight REST API
- No code rewrite needed

### Option 2: JavaScript (Express)
- Full-stack JavaScript
- Would require rewriting chess logic
- Faster for simple requests

**Recommendation:** Python with Flask (reuses existing chess engine)

## HTMX Integration (Planned)

The frontend is structured to easily integrate HTMX for server-driven interactivity:

- Move history div can be swapped with HTMX responses
- Game status updates can be pushed from server
- Minimal JavaScript modifications needed

Example HTMX integration:
```html
<div id="move-history"
     hx-get="/api/move-history"
     hx-trigger="every 2s">
    <!-- Server updates this -->
</div>
```

## Customization

### Change Board Theme
Edit `boardConfig.pieceTheme` in `js/board.js`:
```javascript
pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
```

### Modify Colors
Tailwind colors can be changed directly in `index.html` or add custom CSS in `css/styles.css`.

### Board Size
The board is responsive and adjusts automatically. Max sizes are defined in `css/styles.css`:
```css
#board {
    max-width: 600px; /* Adjust as needed */
}
```

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive
- Requires JavaScript enabled

## Development Notes

- **Minimal JavaScript** - Core logic handled server-side
- **Semantic HTML** - Proper structure and accessibility
- **Modular CSS** - Tailwind utilities + custom styles
- **API-Ready** - Structured for easy backend integration

## Next Steps

1. ✅ Frontend complete
2. ⏳ Build REST API backend (Python/Flask recommended)
3. ⏳ Connect frontend to backend
4. ⏳ Add HTMX for enhanced interactivity
5. ⏳ Deploy to production

## License

Part of the PyChess Engine project.
