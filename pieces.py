import copy
from enum import Enum

import constants as c

class Coord(Enum):
    ROW = 0
    COL = 1

class Piece:
    def __init__(self, name, pos, side):
        self.name = name
        self.pos = pos
        self.side = side

    def __str__(self):
        START_CHAR = 64
        row, col = self.pos
        return f"{self.side.value}{self.name}({chr(START_CHAR + col + 1)}{row + 1})"

    def opponent_piece(self, piece):
        return piece.side != self.side

    def _generic_moves(self, board, radius, row_incr, col_incr):
        legal = []
        cur_pos = list(self.pos)
        while abs(self.pos[0] - cur_pos[0]) + abs(self.pos[1] - cur_pos[1]) < radius:
            cur_pos[0] += row_incr
            cur_pos[1] += col_incr
            
            if (cur_pos[Coord.ROW.value] < 0
                    or cur_pos[Coord.ROW.value] >= c.SIZE
                    or cur_pos[Coord.COL.value] < 0
                    or cur_pos[Coord.COL.value] >= c.SIZE):
                break

            cur_pos_tuple = tuple(cur_pos)
            if board.occupied(cur_pos):
                if self.opponent_piece(board.get_piece(cur_pos)):
                    legal.append(cur_pos_tuple)  # you are permitted to land on an opponent
                break
            legal.append(cur_pos_tuple)
        return legal

    def vertical_moves(self, board, radii):
        up, down = radii
        up_moves = self._generic_moves(board, up, row_incr=1, col_incr=0)
        down_moves = self._generic_moves(board, down, row_incr=-1, col_incr=0)
        return set(up_moves + down_moves)

    def horizontal_moves(self, board, radii):
        left, right = radii
        left_moves = self._generic_moves(board, left, row_incr=0, col_incr=-1)
        right_moves = self._generic_moves(board, right, row_incr=0, col_incr=1)
        return set(left_moves + right_moves)

    def diagonal_moves(self, board, radii):
        up_left, up_right, down_left, down_right = radii
        up_left_moves = self._generic_moves(board, up_left, row_incr=1, col_incr=-1)
        up_right_moves = self._generic_moves(board, up_right, row_incr=1, col_incr=1)
        down_left_moves = self._generic_moves(board, down_left, row_incr=-1, col_incr=-1)
        down_right_moves = self._generic_moves(board, down_right, row_incr=-1, col_incr=1)
        return set(up_left_moves + up_right_moves + down_left_moves + down_right_moves)

    def _legal_moves(self, board, radius):
        up_left, up, up_right, \
        left, right, \
        down_left, down, down_right = radius

        # no piece has diagonal radial disparity
        assert (up_left, down_right) == (up_right, down_left)

        vertical_legal = self.vertical_moves(board, (up, down))
        horizontal_legal = self.horizontal_moves(board, (left, right))
        diagonal_legal = self.diagonal_moves(
            board, 
            (up_left, up_right, down_left, down_right)
        )

        return set.union(vertical_legal, horizontal_legal, diagonal_legal)

class Pawn(Piece):
    def __init__(self, pos, side):
        super(Pawn, self).__init__("P", pos, side)
        self.previously_moved = False

    def legal_moves(self, board):
        forward = 1 if self.previously_moved else 2
        cur_row, cur_col = self.pos

        top_left = board.get_piece((cur_row + 1, cur_col - 1))
        top_right = board.get_piece((cur_row + 1, cur_col + 1))
        top_left_r = 1 if top_left is not None and self.opponent_piece(top_left) else 0
        top_right_r = 1 if top_right is not None and self.opponent_piece(top_right) else 0

        if self.side == c.GameSide.WHITE: 
            radius = [
                top_left_r, forward, top_right_r,
                0,    0,
                0, 0, 0
            ]
        else:
            radius = [
                0, 0, 0,
                0,    0,
                top_left_r, forward, top_right_r
            ]
        return self._legal_moves(board, radius)

class Rook(Piece):
    def __init__(self, pos, side):
        super(Rook, self).__init__("R", pos, side)
        
    def legal_moves(self, board):
        radius = [
            0, 8, 0,
            8,    8,
            0, 8, 0
        ]
        return self._legal_moves(board, radius)

class Knight(Piece):
    def __init__(self, pos, side):
        super(Knight, self).__init__("N", pos, side)
        
    def legal_moves(self, board):
        deltas = [
            (1, 2), (1, -2),
            (-1, 2), (1, -2),
            (2, 1), (-2, 1),
            (2, -1), (-2, -1),
        ]

        possible_moves = set()
        for delta in deltas:
            possible_move = (self.pos[0] + delta[0], self.pos[1] + delta[1])
            if 0 <= possible_move[0] < c.SIZE and 0 <= possible_move[1] < c.SIZE:
                if board.occupied(possible_move):
                    if self.opponent_piece(board.get_piece(possible_move)):
                        possible_moves.add(possible_move)
                else: 
                    possible_moves.add(possible_move)
        return possible_moves

class Bishop(Piece):
    def __init__(self, pos, side):
        super(Bishop, self).__init__("B", pos, side)
        
    def legal_moves(self, board):
        radius = [
            8, 0, 8,
            0,    0,
            8, 0, 8
        ]
        return self._legal_moves(board, radius)

class Queen(Piece):
    def __init__(self, pos, side):
        super(Queen, self).__init__("Q", pos, side)
        
    def legal_moves(self, board):
        radius = [
            8, 8, 8,
            8,    8,
            8, 8, 8
        ]
        return self._legal_moves(board, radius)

class King(Piece):
    def __init__(self, pos, side):
        super(King, self).__init__("K", pos, side)
        
    def legal_moves(self, board):
        radius = [
            1, 1, 1,
            1,    1,
            1, 1, 1
        ]
        return self._legal_moves(board, radius)