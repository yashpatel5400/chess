import constants as c
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
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
        return "\n".join(board_rep)

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
                    self.raw_board[row ][col] = piece_type(
                        (row, col), 
                        game_side_rows[row]
                    )

    def get_piece(self, pos):
        row, col = pos
        return self.raw_board[row][col]

    def occupied(self, pos):
        return self.get_piece(pos) is not None

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
        self.side = c.GameSide.WHITE if self.side == c.GameSide.BLACK else c.GameSide.BLACK

if __name__ == "__main__":
    board = Board()
    white_pawn = board.get_piece((1, 2))
    white_knight = board.get_piece((0, 1))
    white_bishop = board.get_piece((0, 2))

    black_pawn = board.get_piece((6, 2))

    print(white_pawn.legal_moves(board)) # should be (3, 2), (2, 2)
    print(white_knight.legal_moves(board)) # should be ((2, 0), (2, 2))
    print(white_bishop.legal_moves(board)) # should be empty
    print(black_pawn.legal_moves(board)) # should be ((4, 2), (5, 2))

    board.make_move((3, 2), (4, 2)) # should complain about empty tile
    board.make_move((7, 2), (6, 2)) # should complain about manipulating black piece
    board.make_move((1, 2), (4, 2)) # should complain about illegal movement
    board.make_move((1, 2), (3, 2)) # should work
    board.make_move((3, 2), (4, 2)) # should complain about manipulating white piece
