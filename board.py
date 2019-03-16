from enum import Enum 

from pieces import Pawn, Rook, Knight, Bishop, Queen, King

ROWS = 8
COLS = 8

class GameSide(Enum):
    WHITE = "W"
    BLACK = "B"

class Board:
    def __init__(self):
        self._init_board()
        self.side = GameSide.WHITE

    def __str__(self):
        board_rep = []
        for row in self.raw_board:
            cur_row = []
            for piece in row:
                piece_rep = piece.__str__() if piece is not None else "_" * 6
                cur_row.append(piece_rep)
            board_rep.append(" ".join(cur_row))
        return "\n".join(board_rep)

    def _init_board(self):
        self.raw_board = [[None] * COLS for _ in range(ROWS)]
        game_side_rows = {
            1: GameSide.WHITE, 
            2: GameSide.WHITE, 
            7: GameSide.BLACK,
            8: GameSide.WHITE, 
        }

        rows_col_to_piece = {
            (1, 8): {
                1: Rook,
                2: Knight,
                3: Bishop,
                4: Queen,
                5: King,
                6: Bishop,
                7: Knight,
                8: Rook
            },
            (2, 7):  {
                1: Pawn,
                2: Pawn,
                3: Pawn,
                4: Pawn,
                5: Pawn,
                6: Pawn,
                7: Pawn,
                8: Pawn
            }, 
        }

        for rows in rows_col_to_piece:
            col_to_piece = rows_col_to_piece[rows]
            for row in rows:
                for col in col_to_piece:
                    piece_type = col_to_piece[col]
                    self.raw_board[row - 1][col - 1] = piece_type(
                        (row - 1, col - 1), 
                        game_side_rows[row]
                    )
        
    def insert_piece(self, piece, pos):
        pass

    def get_piece(self, pos):
        row, col = pos
        return self.raw_board[row][col]

    def occupied(self, pos):
        return self.get_piece(pos) is None

if __name__ == "__main__":
    board = Board()
    print(board)