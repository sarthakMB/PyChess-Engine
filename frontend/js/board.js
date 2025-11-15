/**
 * PyChess Engine - Frontend Board Logic
 * Minimal JavaScript for board initialization and UI interactions
 * Game logic handled by server-side REST API
 */

// API Configuration (update when backend is ready)
const API_BASE_URL = 'http://localhost:5000/api';

// Game State
let gameState = {
    board: null,
    currentTurn: 'white',
    moveCount: 0,
    status: 'In Progress',
    fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    moveHistory: [],
    capturedPieces: {
        white: [],
        black: []
    }
};

// Initialize board configuration
const boardConfig = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
    pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
};

// Initialize the chessboard
let board = null;

// DOM Ready
$(document).ready(function() {
    initializeBoard();
    attachEventHandlers();
    updateUI();
});

/**
 * Initialize the chessboard
 */
function initializeBoard() {
    board = Chessboard('board', boardConfig);
    gameState.board = board;
}

/**
 * Attach event handlers to buttons
 */
function attachEventHandlers() {
    $('#new-game').on('click', handleNewGame);
    $('#flip-board').on('click', handleFlipBoard);
}

/**
 * Handle drag start - validate if piece can be moved
 */
function onDragStart(source, piece, position, orientation) {
    // Don't allow moves if game is over
    if (gameState.status === 'Checkmate' || gameState.status === 'Stalemate') {
        return false;
    }

    // Only allow moving pieces of the current turn
    if ((gameState.currentTurn === 'white' && piece.search(/^b/) !== -1) ||
        (gameState.currentTurn === 'black' && piece.search(/^w/) !== -1)) {
        return false;
    }

    return true;
}

/**
 * Handle piece drop - validate and make move
 * This will eventually call the REST API
 */
function onDrop(source, target) {
    // Prevent dropping on same square
    if (source === target) {
        return 'snapback';
    }

    // TODO: Call REST API to validate and make move
    // For now, just simulate a successful move
    handleMove(source, target);
}

/**
 * Handle snap end - update board after animation
 */
function onSnapEnd() {
    board.position(board.position());
}

/**
 * Handle move - This will be replaced with API call
 * @param {string} source - Source square (e.g., 'e2')
 * @param {string} target - Target square (e.g., 'e4')
 */
function handleMove(source, target) {
    // TODO: Replace with actual API call
    // For now, just accept the move and update UI

    // Simulate move recording
    const moveNotation = `${source}-${target}`;
    gameState.moveCount++;

    // Add to move history
    addMoveToHistory(moveNotation, gameState.currentTurn);

    // Toggle turn
    gameState.currentTurn = gameState.currentTurn === 'white' ? 'black' : 'white';

    // Update UI
    updateUI();

    // Show success feedback
    showFeedback('Move successful!', 'success');
}

/**
 * Handle new game button
 */
function handleNewGame() {
    // Reset game state
    gameState = {
        board: board,
        currentTurn: 'white',
        moveCount: 0,
        status: 'In Progress',
        fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        moveHistory: [],
        capturedPieces: {
            white: [],
            black: []
        }
    };

    // Reset board to starting position
    board.start();

    // Clear move history
    $('#move-history').html('<p class="text-slate-500 text-sm italic">No moves yet</p>');

    // Clear captured pieces
    $('#white-captured').html('');
    $('#black-captured').html('');

    // Update UI
    updateUI();

    showFeedback('New game started!', 'info');
}

/**
 * Handle flip board button
 */
function handleFlipBoard() {
    board.flip();
    showFeedback('Board flipped', 'info');
}

/**
 * Add move to history display
 */
function addMoveToHistory(move, color) {
    gameState.moveHistory.push({ move, color });

    const moveNumber = Math.ceil(gameState.moveHistory.length / 2);
    const moveClass = color === 'white' ? 'white-move' : 'black-move';
    const colorLabel = color.charAt(0).toUpperCase() + color.slice(1);

    // Remove "no moves" message if present
    if (gameState.moveHistory.length === 1) {
        $('#move-history').html('');
    }

    const moveEntry = `
        <div class="move-entry ${moveClass}">
            <div class="flex justify-between items-center">
                <span class="text-slate-400 text-sm">${moveNumber}. ${colorLabel}</span>
                <span class="font-mono text-slate-200">${move}</span>
            </div>
        </div>
    `;

    $('#move-history').append(moveEntry);

    // Scroll to bottom
    $('#move-history').scrollTop($('#move-history')[0].scrollHeight);
}

/**
 * Update UI elements
 */
function updateUI() {
    // Update turn indicator
    $('#current-turn').text(gameState.currentTurn.charAt(0).toUpperCase() + gameState.currentTurn.slice(1));

    // Update move count
    $('#move-count').text(gameState.moveCount);

    // Update game status
    const statusElement = $('#game-status');
    statusElement.text(gameState.status);

    // Apply status-specific styling
    statusElement.removeClass('text-green-400 text-red-500 text-yellow-400 status-check status-checkmate');

    if (gameState.status === 'Check') {
        statusElement.addClass('text-yellow-400 status-check');
    } else if (gameState.status === 'Checkmate') {
        statusElement.addClass('text-red-500 status-checkmate');
    } else if (gameState.status === 'Stalemate') {
        statusElement.addClass('text-yellow-400');
    } else {
        statusElement.addClass('text-green-400');
    }

    // Update FEN string
    $('#fen-string').text(gameState.fen);
}

/**
 * Show feedback message
 */
function showFeedback(message, type = 'info') {
    const feedbackElement = $('#move-feedback');
    const feedbackText = $('#feedback-text');

    feedbackText.text(message);
    feedbackElement.removeClass('hidden success error info');
    feedbackElement.addClass(type);

    // Auto-hide after 3 seconds
    setTimeout(() => {
        feedbackElement.addClass('hidden');
    }, 3000);
}

/**
 * Add captured piece to display
 */
function addCapturedPiece(piece, color) {
    const pieceColor = color === 'white' ? 'w' : 'b';
    const pieceSymbol = piece.toLowerCase();
    const pieceImg = `https://chessboardjs.com/img/chesspieces/wikipedia/${pieceColor}${pieceSymbol.toUpperCase()}.png`;

    const capturedDiv = color === 'white' ? '#white-captured' : '#black-captured';

    $(capturedDiv).append(`
        <div class="captured-piece" style="background-image: url('${pieceImg}')"></div>
    `);

    gameState.capturedPieces[color].push(piece);
}

/**
 * API Functions - To be implemented when backend is ready
 */

// Make a move via API
async function apiMakeMove(from, to) {
    try {
        const response = await fetch(`${API_BASE_URL}/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                from: from,
                to: to
            })
        });

        if (!response.ok) {
            throw new Error('Move failed');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showFeedback('Failed to make move', 'error');
        return null;
    }
}

// Get current board state from API
async function apiFetchBoardState() {
    try {
        const response = await fetch(`${API_BASE_URL}/board`);

        if (!response.ok) {
            throw new Error('Failed to fetch board state');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

// Start a new game via API
async function apiNewGame() {
    try {
        const response = await fetch(`${API_BASE_URL}/new-game`, {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error('Failed to start new game');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

// Get valid moves for a piece via API
async function apiGetValidMoves(position) {
    try {
        const response = await fetch(`${API_BASE_URL}/valid-moves/${position}`);

        if (!response.ok) {
            throw new Error('Failed to get valid moves');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

// Helper: Convert algebraic notation to Position(row, col)
// Chessboard.js uses algebraic (e.g., 'e2'), Python backend uses Position(row, col)
function algebraicToPosition(algebraic) {
    // e.g., 'e2' -> Position(6, 4)
    const col = algebraic.charCodeAt(0) - 'a'.charCodeAt(0); // 0-7
    const row = 8 - parseInt(algebraic[1]); // 0-7, inverted
    return { row, col };
}

function positionToAlgebraic(row, col) {
    // e.g., Position(6, 4) -> 'e2'
    const file = String.fromCharCode('a'.charCodeAt(0) + col);
    const rank = 8 - row;
    return `${file}${rank}`;
}
