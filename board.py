class Board:
    def __init__(self,fen = None):
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        if fen is None:
            self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        else:
            self.fen = fen
        
        self.game_history = [fen]

        self.white_to_play = True
        self.white_king_side_castle = True
        self.white_queen_side_castle = True
        self.black_king_side_castle = True
        self.black_queen_side_castle = True
        self.en_passant = None
        self.halfmove_number = 0
        self.fullmove_number = 1

        self.piece_list = []
        self._construct_board(self.fen)

    def __str__(self):
        ret = []
        for row in self.board:  
            ret.append(' '.join([str(piece) for piece in row]))
        return '\n'.join(ret)
    


    def move_piece(self, old_position, new_position): #IMPLEMENTED
        #checks
        if self.board[old_position.row][old_position.col] == " ":
            print("No piece to move.")
            return
        if not self._is_move_valid(old_position,new_position):
            print("Invalid move.")
            return
        
        #move logic
        if self.board[new_position.row][new_position.col] != " ":
            self.board[new_position.row][new_position.col].position = Position(-1,-1)
            self.board[old_position.row][old_position.col].position = new_position
            self.board[new_position.row][new_position.col] = self.board[old_position.row][old_position.col]
            self.board[old_position.row][old_position.col] = " "
        else:
            self.board[old_position.row][old_position.col].position = new_position
            self.board[new_position.row][new_position.col] = self.board[old_position.row][old_position.col]
            self.board[old_position.row][old_position.col] = " "

        #updates 
        self.halfmove_number += 1
        if self.white_to_play:
            self.white_to_play = False
        else:
            self.white_to_play = True
            self.fullmove_number += 1
        self.check_castling()
        self.check_en_passant()
        
        #update fen
        self.update_fen()
        self.game_history.append(self.fen)
        
        return
    
    def _is_move_valid(self,old_position,new_position): #IMPLEMENT THIS
        if old_position == new_position:
            print("Old and new position are the same.")
            return False
        print("valid moves: ",self._valid_moves(old_position))
        if new_position in self._valid_moves(old_position):
            return True
        else:
            print("Invalid move.")  
            return False


    def _valid_moves(self,position):
        #get all moves for a piece at a position, checking for checks
        if self.board[position.row][position.col] == " ":
            return []
        if self._discovered_check(position):
            return []
        else:
            piece = self.board[position.row][position.col]
            return piece.possible_moves(self.board)

    def _discovered_check(self,position): #IMPLEMENT THIS
        return False

    # def _get_moves(self,position): #IMPLEMENT THIS
    #     #get all moves for a piece at a position, not checking for checks
    #     if position == " ":
    #         return []
    #     piece = self.board[position.row][position.col]
    #     return piece.possible_moves(self.board)



        

    def _construct_board(self,fen): #IMPLEMENT THIS
        rows = fen.split('/')
        rows[-1] = rows[-1].split(' ')[0]
        for row_num, row in enumerate(rows):
            it = 0
            for char in row:
                if char.isdigit():
                    for _ in range(int(char)):
                        self.board[row_num][it] = " "
                        it += 1
                else:
                    if char.lower() == 'p':
                        self.board[row_num][it] = Pawn(not char.islower(), Position(row_num, it))
                    elif char.lower() == 'r':
                        self.board[row_num][it] = Rook(not char.islower(), Position(row_num, it))
                    elif char.lower() == 'n':
                        self.board[row_num][it] = Knight(not char.islower(), Position(row_num, it))
                    elif char.lower() == 'b':
                        self.board[row_num][it] = Bishop(not char.islower(), Position(row_num, it))
                    elif char.lower() == 'q':
                        self.board[row_num][it] = Queen(not char.islower(), Position(row_num, it))
                    elif char.lower() == 'k':
                        self.board[row_num][it] = King(not char.islower(), Position(row_num, it))
                    self.piece_list.append(self.board[row_num][it])
                    it += 1

    def update_fen(self): #IMPLEMENT THIS
        pass

class Position: #according to the the board list coordinates, row = 0 is back rank of black.
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return f"{chr(ord('a')+self.col)}{8-self.row}"
    def __repr__(self):
        return f"({self.row}, {self.col})"
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

class Piece:
    def __init__(self, is_white, position):
        self.is_white = is_white
        self.position = position

class Pawn(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)

    def __str__(self):
        return 'P' if self.is_white else 'p'
    
    def possible_moves(self,board): #all moves that are possible for a pawn not checking for checks
        moves = []
        if self.is_white:
            if board[self.position.row - 1][self.position.col] == " ":
                moves.append(Position(self.position.row - 1, self.position.col))
            if self.position.row == 6:
                if board[self.position.row - 2][self.position.col] == " ":
                    moves.append(Position(self.position.row - 2, self.position.col))
            if self.position.col > 0:
                if board[self.position.row - 1][self.position.col - 1] != " " and not board[self.position.row - 1][self.position.col - 1].is_white:
                    moves.append(Position(self.position.row - 1, self.position.col - 1))
            if self.position.col < 7:
                if board[self.position.row - 1][self.position.col + 1] != " " and not board[self.position.row - 1][self.position.col + 1].is_white:
                    moves.append(Position(self.position.row - 1, self.position.col + 1))
        else:
            if board[self.position.row + 1][self.position.col] == " ":
                moves.append(Position(self.position.row + 1, self.position.col))
            if self.position.row == 1:
                if board[self.position.row + 2][self.position.col] == " ":
                    moves.append(Position(self.position.row + 2, self.position.col))
            if self.position.col > 0:
                if board[self.position.row + 1][self.position.col - 1] != " " and board[self.position.row + 1][self.position.col - 1].is_white:
                    moves.append(Position(self.position.row + 1, self.position.col - 1))
            if self.position.col < 7:
                if board[self.position.row + 1][self.position.col + 1] != " " and board[self.position.row + 1][self.position.col + 1].is_white:
                    moves.append(Position(self.position.row + 1, self.position.col + 1))
        return moves
                    



class Rook(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)
        
    def __str__(self):
        return 'R' if self.is_white else 'r'
    
    def possible_moves(self,board):
        moves = []
        deltas = [(1,0),(-1,0),(0,1),(0,-1)]
        for delta in deltas:
            for i in range(1,8):
                if self.position.row + delta[0] * i < 0 or self.position.row + delta[0] * i > 7 or self.position.col + delta[1] * i < 0 or self.position.col + delta[1] * i > 7:
                    break
                if board[self.position.row + delta[0] * i][self.position.col + delta[1] * i] == " ":
                    moves.append(Position(self.position.row + delta[0] * i, self.position.col + delta[1] * i))
                elif board[self.position.row + delta[0] * i][self.position.col + delta[1] * i].is_white != self.is_white:
                    moves.append(Position(self.position.row + delta[0] * i, self.position.col + delta[1] * i))
                    break   
                else:
                    break
        return moves

class Knight(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)

    def __str__(self):
        return 'N' if self.is_white else 'n'
    
    def possible_moves(self,board):
        moves = []
        deltas = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for delta in deltas:
            if self.position.row + delta[0] < 0 or self.position.row + delta[0] > 7 or self.position.col + delta[1] < 0 or self.position.col + delta[1] > 7:
                continue
            if board[self.position.row + delta[0]][self.position.col + delta[1]] == " ":
                moves.append(Position(self.position.row + delta[0], self.position.col + delta[1]))
            elif board[self.position.row + delta[0]][self.position.col + delta[1]].is_white != self.is_white:
                moves.append(Position(self.position.row + delta[0], self.position.col + delta[1]))
        return moves

class Bishop(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)

    def __str__(self):
        return 'B' if self.is_white else 'b'
    
    def possible_moves(self,board):
        moves = []
        deltas = [(1,1),(1,-1),(-1,1),(-1,-1)]
        for delta in deltas:
            for i in range(1,8):    
                if self.position.row + delta[0] * i < 0 or self.position.row + delta[0] * i > 7 or self.position.col + delta[1] * i < 0 or self.position.col + delta[1] * i > 7:
                    break
                if board[self.position.row + delta[0] * i][self.position.col + delta[1] * i] == " ":
                    moves.append(Position(self.position.row + delta[0] * i, self.position.col + delta[1] * i))
                elif board[self.position.row + delta[0] * i][self.position.col + delta[1] * i].is_white != self.is_white:
                    moves.append(Position(self.position.row + delta[0] * i, self.position.col + delta[1] * i))
                    break
                else:
                    break
        return moves
    
class Queen(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)

    def __str__(self):
        return 'Q' if self.is_white else 'q'
    
    def possible_moves(self,board):
        moves = []
        deltas = [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]
        for delta in deltas:
            for i in range(1,8):
                if self.position.row + delta[0] * i < 0 or self.position.row + delta[0] * i > 7 or self.position.col + delta[1] * i < 0 or self.position.col + delta[1] * i > 7:
                    break
                if board[self.position.row + delta[0] * i][self.position.col + delta[1] * i] == " ":
                    moves.append(Position(self.position.row + delta[0] * i, self.position.col + delta[1] * i))
                elif board[self.position.row + delta[0] * i][self.position.col + delta[1] * i].is_white != self.is_white:
                    moves.append(Position(self.position.row + delta[0] * i, self.position.col + delta[1] * i))
                    break   
                else:
                    break
        return moves
    
class King(Piece):
    def __init__(self, is_white, position):
        super().__init__(is_white, position)

    def __str__(self):
        return 'K' if self.is_white else 'k'

    def possible_moves(self,board):
        moves = []
        deltas = [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]
        for delta in deltas:
            if self.position.row + delta[0] < 0 or self.position.row + delta[0] > 7 or self.position.col + delta[1] < 0 or self.position.col + delta[1] > 7:
                continue
            if board[self.position.row + delta[0]][self.position.col + delta[1]] == " ":
                moves.append(Position(self.position.row + delta[0], self.position.col + delta[1]))
            elif board[self.position.row + delta[0]][self.position.col + delta[1]].is_white != self.is_white:
                moves.append(Position(self.position.row + delta[0], self.position.col + delta[1]))
        return moves

def main():
    board = Board()
    print(board)
    print(board.board[1][4].possible_moves(board.board))
    print(board._is_move_valid(Position(1,4),Position(2,4)))
if __name__ == "__main__":
    main()

