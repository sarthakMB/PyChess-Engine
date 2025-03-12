import random
import copy

class Board:
    def __init__(self,fen = None):
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        if fen is None:
            self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        else:
            self.fen = fen
        
        self.game_history_fen = [fen]

        self.white_to_play = True
        self.white_king_side_castle = True
        self.white_queen_side_castle = True
        self.black_king_side_castle = True
        self.black_queen_side_castle = True
        self.en_passant = None
        self.halfmove_number = 0
        self.fullmove_number = 1

        self.piece_list = []
        self.position_list = []
        self._construct_board(self.fen)

        self.state = {'board':self.board.copy(),
                      'white_to_play':self.white_to_play,
                      'white_king_side_castle':self.white_king_side_castle,
                      'white_queen_side_castle':self.white_queen_side_castle,
                      'black_king_side_castle':self.black_king_side_castle,
                      'black_queen_side_castle':self.black_queen_side_castle,
                      'en_passant':self.en_passant,
                      'halfmove_number':self.halfmove_number,
                      'fullmove_number':self.fullmove_number,
                      'position_list': copy.deepcopy(self.position_list)}
        self.game_history_state = [self.state]

    def __str__(self):
        ret = []
        white_killed = []
        black_killed = []
        for row in self.board:  
            ret.append("| " + ' '.join([piece.__str__() for piece in row]) + " |")

        for piece in self.piece_list:
            if piece.is_white and piece.position == Position(-1,-1):
                white_killed.append(piece)
            elif not piece.is_white and piece.position == Position(-1,-1):
                black_killed.append(piece)

        ret[0] = ret[0] + "    " +  " ".join([str(piece) for piece in white_killed])
        ret[7] = ret[7] + "    " + " ".join([str(piece) for piece in black_killed])
        ret.append("")
        ret.append("| a b c d e f g h |")

        str_board = '\n'.join(ret)
        return str_board

    

    def move_piece(self, old_position, new_position): #DONE
        kill = False
        killed_piece = None
        killed_piece_position = None
        #checks
        if self.board[old_position.row][old_position.col] == " ":
            print("No piece to move.")
            return (False,None,None)
        if not self._is_move_valid(old_position,new_position):
            print("Invalid move.")
            return (False,None,None)
        
        #move logic
        if self.board[new_position.row][new_position.col] != " ":
            kill = True
            killed_piece = self.board[new_position.row][new_position.col]
            killed_piece_position = killed_piece.position
            self.board[new_position.row][new_position.col].position = Position(-1,-1)
            self.board[old_position.row][old_position.col].position = new_position
            self.board[new_position.row][new_position.col] = self.board[old_position.row][old_position.col]
            self.board[old_position.row][old_position.col] = " "
        else:
            self.board[old_position.row][old_position.col].position = new_position
            self.board[new_position.row][new_position.col] = self.board[old_position.row][old_position.col]
            self.board[old_position.row][old_position.col] = " "

        #board state updates 
        self.halfmove_number += 1
        if self.white_to_play:
            self.white_to_play = False
        else:
            self.white_to_play = True
            self.fullmove_number += 1
        self._check_castling()
        self._check_en_passant()
        
        #update fen
        self._update_fen()
        self._save_state()
        
        return (kill,killed_piece,killed_piece_position)
    
    def _save_state(self):
        state_var = {'board':self.board.copy(),
                      'white_to_play':self.white_to_play,
                      'white_king_side_castle':self.white_king_side_castle,
                      'white_queen_side_castle':self.white_queen_side_castle,
                      'black_king_side_castle':self.black_king_side_castle,
                      'black_queen_side_castle':self.black_queen_side_castle,
                      'en_passant':self.en_passant,
                      'halfmove_number':self.halfmove_number,
                      'fullmove_number':self.fullmove_number,
                      'position_list': copy.deepcopy(self.position_list)}
        assert(len(self.game_history_state) >= self.halfmove_number)
        self.game_history_state = self.game_history_state[:self.halfmove_number]
        self.game_history_state.append(state_var)

    def _restore_state(self,state):
        self.board = state['board']
        self.white_to_play = state['white_to_play']
        self.white_king_side_castle = state['white_king_side_castle']
        self.white_queen_side_castle = state['white_queen_side_castle']
        self.black_king_side_castle = state['black_king_side_castle']
        self.black_queen_side_castle = state['black_queen_side_castle'] 
        self.en_passant = state['en_passant']
        self.halfmove_number = state['halfmove_number']
        self.fullmove_number = state['fullmove_number']
        # self.position_list = state['position_list']
        for idx,val in enumerate(state['position_list']):
            self.piece_list[idx].position.row = val.row
            self.piece_list[idx].position.col = val.col

    def _restore_history_last(self):
        if self.halfmove_number > 0:
            self._restore_state(self.game_history_state[self.halfmove_number-1])
        else:
            print("No more history.")

    def _restore_history_next(self):
        if self.halfmove_number < len(self.game_history_state):
            self._restore_state(self.game_history_state[self.halfmove_number+1])
        else:
            print("No more history.")
    
    def _is_move_valid(self,old_position,new_position): #DONE
        if old_position == new_position:
            # print("Old and new position are the same.")xs
            return False
        # print("valid moves: ",self._valid_moves(old_position))
        if new_position in self._valid_moves(old_position):
            return True
        else:
            # print("Invalid move.")  
            return False

    def _valid_moves(self,position): #DONE
        assert(position != Position(-1,-1))
        #get all moves for a piece at a position, checking for checks
        if self.board[position.row][position.col] == " ":
            return []
        piece = self.board[position.row][position.col]
        ret = []
        for move in piece.possible_moves(self.board):
            if not self._king_checked_after_move(position,move):
                ret.append(move)
        return ret

    def _king_checked_after_move(self,old_position,new_position): #DONE
        assert(old_position != Position(-1,-1) and new_position != Position(-1,-1))
        #move
        killed_piece = None
        if self.board[new_position.row][new_position.col] != " ":
            killed_piece = self.board[new_position.row][new_position.col]
            self.board[new_position.row][new_position.col].position = Position(-1,-1)
            self.board[old_position.row][old_position.col].position = new_position
            self.board[new_position.row][new_position.col] = self.board[old_position.row][old_position.col]
            self.board[old_position.row][old_position.col] = " "
        else:
            self.board[old_position.row][old_position.col].position = new_position
            self.board[new_position.row][new_position.col] = self.board[old_position.row][old_position.col]
            self.board[old_position.row][old_position.col] = " "

        king_under_check = False
        #logic
        king = None
        for piece in self.piece_list:
            if self.white_to_play == piece.is_white and piece.__str__().lower() == 'k':
                king = piece
                break
        for piece in self.piece_list:
            if piece.is_white != self.white_to_play:
                for move in piece.possible_moves(self.board):
                    if move == king.position:
                        king_under_check = True
                        break
        

        #unmove
        self.board[new_position.row][new_position.col].position = old_position
        self.board[old_position.row][old_position.col] = self.board[new_position.row][new_position.col]
        if killed_piece:
            killed_piece.position = new_position
            self.board[new_position.row][new_position.col] = killed_piece
        else:
            self.board[new_position.row][new_position.col] = " "

        return king_under_check
        

    def _construct_board(self,fen):
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
                    self.position_list.append(self.board[row_num][it].position)
                    it += 1

    def _update_fen(self): #IMPLEMENT THIS
        pass

    def _check_castling(self): #IMPLEMENT THIS
        pass 

    def _check_en_passant(self): #IMPLEMENT THIS
        pass

    def _play_random_move(self): #IMPLEMENT THIS
        legal_piece_moves = []
        for piece in self.piece_list:
            # assert(self.board[piece.position.row][piece.position.col] == piece)
            for move in legal_piece_moves:
                assert(move[0].row < 8 and move[0].col < 8)
                # assert(self.board[move[0].row][move[0].col].is_white == self.white_to_play)            
            if piece.is_white == self.white_to_play and piece.position != Position(-1,-1):
                print(piece.__str__(),end=' ')
                all_piece_moves = self._valid_moves(piece.position)
                for move in all_piece_moves:
                    assert(piece.is_white == self.white_to_play)
                    assert(self._board_vs_piece_list_check())
                    legal_piece_moves.append((piece.position,move))
                    # assert(self.board[legal_piece_moves[-1][0].row][legal_piece_moves[-1][0].col].is_white == self.white_to_play)
                    # assert(legal_piece_moves[-1][0].row >= 0 and legal_piece_moves[-1][0].col >= 0)
                # legal_piece_moves += [(piece.position,move) for move in self._valid_moves(piece.position)]
        assert(len(legal_piece_moves) > 0)
        for move in legal_piece_moves:
            assert(move[0].row < 8 and move[0].col < 8)
            assert(self.board[move[0].row][move[0].col].is_white == self.white_to_play)

            # assert(move[0].row >= 0 and move[0].col >= 0)
            # assert(self.board[move[0].row][move[0].col].position != Position(-1,-1))
            print(self.board[move[0].row][move[0].col].__str__()+": "+move[0].__str__(),'->',move[1].__str__(),end='    ')
        move = random.choice(legal_piece_moves)
        print("\n\nDecided : ",self.board[move[0].row][move[0].col].__str__()+": "+move[0].__str__(),'->',move[1].__str__(),"\n\n")
        self.move_piece(move[0],move[1])

    def is_mate(self): 
        legal_moves = []
        for piece in self.piece_list:
            if piece.is_white == self.white_to_play and piece.position != Position(-1,-1):
                legal_moves.extend(self._valid_moves(piece.position))
        return len(legal_moves) == 0
        


    def is_check(self): 
        king_under_check = False
        king = None
        for piece in self.piece_list:
            if self.white_to_play == piece.is_white and piece.__str__().lower() == 'k':
                king = piece
                break
        for piece in self.piece_list:
            if piece.is_white != self.white_to_play:
                for move in piece.possible_moves(self.board):
                    if move == king.position:
                        king_under_check = True
                        break
        return king_under_check
    
    def is_checkmate(self): 
        return self.is_mate() and self.is_check()
    
    def _board_vs_piece_list_check(self):
        for piece in self.piece_list:
            if piece.position != Position(-1,-1):
                if self.board[piece.position.row][piece.position.col] != piece:
                    return False
        for row in self.board:
            for piece in row:
                if piece != " ":
                    if piece.position == Position(-1,-1):
                        return False
        return True
        


class Position: #according to the the board list coordinates, row = 0 is back rank of black.
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        # return f"{chr(ord('a')+self.col)}{8-self.row}"
        return f"({self.row}, {self.col})"
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
        if self.position == Position(-1,-1) or self.position.row == 0 or self.position.row == 7:
            return moves
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
        if self.position == Position(-1,-1):
            return moves
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
        if self.position == Position(-1,-1):
            return moves
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
        if self.position == Position(-1,-1):
            return moves
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
        if self.position == Position(-1,-1):
            return moves
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
        if self.position == Position(-1,-1):
            return moves
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
    random.seed(1)
    for row in board.board:
        for col in row:
            if col != " ":
                print(col.__str__(),end=' ')
            else:
                print(" ",end=' ')
        print()
    for row in board.board:
        for col in row:
            if col != " ":
                print(col.is_white,end=' ')
            else:
                print(" ",end=' ')
        print()
    for row in board.board:
        for col in row:
            if col != " ":
                print(col.position,end=' ')
            else:
                print(" ",end=' ')
        print()
    # print(board)
    # print("halfmove number:",board.halfmove_number, "  is_mate:",board.is_mate(), "  is_check:",board.is_check(), "  is_white_to_play:",board.white_to_play)
    # print("\n--------------------------------\n")
    # try:
    #     with open("output.txt", "w") as f:
    #         print(board.__str__(),file=f)  # This writes "board" to the file with a newline
    #         print("halfmove number:",board.halfmove_number, "  is_mate:",board.is_mate(), "  is_check:",board.is_check(), "  is_white_to_play:",board.white_to_play,file=f)
    #         print("\n--------------------------------\n",file=f)
    #         f.flush()  # Ensure all data is written to the file
    # except Exception as e:
    #     print(f"An error occurred: {e}")  # Print any error that occurs

    while not board.is_mate() and board._board_vs_piece_list_check():
    # while board._board_vs_piece_list_check():
    # for _ in range(5):
        print("one ",board._board_vs_piece_list_check())
        print_str = "halfmove number: "+str(board.halfmove_number)+ "  is_mate: "+str(board.is_mate())+ "  is_check: "+str(board.is_check()) +"  is_white_to_play: "+str(board.white_to_play)
        print(print_str+"\n")
        print(board)
        print("\n--------------------------------\n")
        try:
            with open("output.txt", "a") as f:
                print(print_str,file=f)
                print(board.__str__(),file=f)  # This writes "board" to the file with a newline
                print("\n--------------------------------\n",file=f)
                f.flush()  # Ensure all data is written to the file
        except Exception as e:
            print(f"An error occurred: {e}")  # Print any error that occurs
        key = "p"
        # input("Enter a key: ")
        if key == 'q':
            break
        elif key == 'b':
            board._restore_history_last()
        elif key == 'n':
            board._restore_history_next()
        else:
            print("two ",board._board_vs_piece_list_check())
            board._play_random_move()
            print("three ",board._board_vs_piece_list_check())
            # print("three1 ",board._board_vs_piece_list_check())
        # if board.is_mate():
        #     print("three1 ",board._board_vs_piece_list_check())
        #     for piece in board.piece_list:
        #         if piece.is_white == board.white_to_play and piece.position != Position(-1,-1):
        #             print(piece.__str__(),end=' ')
        #             print(board._valid_moves(piece.position))
        #     print("three2 ",board._board_vs_piece_list_check())
        print("three3 ",board._board_vs_piece_list_check())
        board.is_mate()
        print("three4 ",board._board_vs_piece_list_check())
        assert(board._board_vs_piece_list_check())
    print("four ",board._board_vs_piece_list_check())
    print_str = "halfmove number: "+str(board.halfmove_number)+ "  is_mate: "+str(board.is_mate())+ "  is_check: "+str(board.is_check()) +"  is_white_to_play: "+str(board.white_to_play)
    print(print_str+"\n")
    print(board)
    print("\n--------------------------------\n")




if __name__ == "__main__":
    main()

