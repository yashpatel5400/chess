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
            0: GameSide.WHITE, 
            1: GameSide.WHITE, 
            6: GameSide.BLACK,
            7: GameSide.WHITE, 
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
                    self.raw_board[row ][col] = piece_type(
                        (row, col), 
                        game_side_rows[row]
                    )

    def get_piece(self, pos):
        row, col = pos
        return self.raw_board[row][col]

    def occupied(self, pos):
        return self.get_piece(pos) is None

if __name__ == "__main__":
    board = Board()
    print(board)
    print(board.get_piece((0, 2))) # should be white bishop