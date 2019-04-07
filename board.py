import constants as c
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.pieces = {
            c.GameSide.WHITE.value: set(),
            c.GameSide.BLACK.value: set(),
        }
        self._init_board()
        self.side = c.GameSide.WHITE
        
    def __str__(self):
        board_rep = []
        for row in self.raw_board:
            cur_row = []
            for piece in row:
                piece_rep = piece.__str__() if piece is not None else "_" * 6
                cur_row.append(piece_rep)
            board_rep.append(" ".join(cur_row))
        return "\n".join(board_rep[::-1])

    def _init_board(self):
        self.raw_board = [[None] * c.SIZE for _ in range(c.SIZE)]
        game_side_rows = {
            0: c.GameSide.WHITE, 
            1: c.GameSide.WHITE, 
            6: c.GameSide.BLACK,
            7: c.GameSide.BLACK, 
        }

        rows_col_to_piece = {
            (0, 7): {
                0: Rook,
                1: Knight,
                2: Bishop,
                3: Queen,
                4: King,
                5: Bishop,
                6: Knight,
                7: Rook
            },
            (1, 6):  {
                0: Pawn,
                1: Pawn,
                2: Pawn,
                3: Pawn,
                4: Pawn,
                5: Pawn,
                6: Pawn,
                7: Pawn
            }, 
        }

        for rows in rows_col_to_piece:
            col_to_piece = rows_col_to_piece[rows]
            for row in rows:
                for col in col_to_piece:
                    piece_type = col_to_piece[col]
                    piece = piece_type(
                        (row, col), 
                        game_side_rows[row]
                    )

                    self.raw_board[row][col] = piece
                    self.pieces[game_side_rows[row].value].add(piece)


    def get_piece(self, pos):
        row, col = pos
        return self.raw_board[row][col]

    def occupied(self, pos):
        return self.get_piece(pos) is not None

    def in_check(self):
        opposite_side = c.GameSide.WHITE if self.side == c.GameSide.BLACK else c.GameSide.BLACK
        opposite_pieces = self.pieces[opposite_side.value]
        # TODO: Figure out caching scheme to avoid recompute each time
        for piece in opposite_pieces:
            for move in piece.legal_moves(self):
                capture_piece = self.get_piece(move)
                if capture_piece is not None:
                    if isinstance(capture_piece, King) and capture_piece.side == self.side:
                        return True
        return False

    def make_move(self, cur_pos, new_pos):
        if not self.occupied(cur_pos):
            print("Illegal move: position must be non-empty to make move!")
            return

        piece = self.get_piece(cur_pos)
        if piece.side != self.side:
            print("Illegal move: only move pieces of your own color!")
            return

        legal_moves = piece.legal_moves(self)
        if new_pos not in legal_moves:
            print(f"Illegal move: {new_pos} not in {legal_moves}!")
            return

        self.raw_board[cur_pos[0]][cur_pos[1]] = None
        self.raw_board[new_pos[0]][new_pos[1]] = piece
        
        if self.in_check():
            print(f"Illegal move: move results in a check!")
            self.raw_board[new_pos[0]][new_pos[1]] = None
            self.raw_board[cur_pos[0]][cur_pos[1]] = piece
            return            

        piece.pos = new_pos
        self.side = c.GameSide.WHITE if self.side == c.GameSide.BLACK else c.GameSide.BLACK
        print(f"{self.side.value} to move!")

if __name__ == "__main__":
    board = Board()
    white_pawn = board.get_piece((1, 2))
    white_knight = board.get_piece((0, 1))
    white_bishop = board.get_piece((0, 2))

    black_pawn = board.get_piece((6, 2))

    board.make_move((1, 4), (3, 4))  # white E pawn
    board.make_move((6, 5), (4, 5))  # black F pawn
    board.make_move((0, 3), (4, 7))  # white queen 
    board.make_move((6, 0), (4, 0))  # error: king is in check
    print(board)
    board.make_move((6, 6), (5, 6))  # legal: (blocks white queen)
    