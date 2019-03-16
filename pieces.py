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
        return piece.side == self.side

    def _generic_moves(self, board, radius, fixed_coord):
        r_pos, r_neg = radius # radius of forward and backward movement resp.
        fixed = self.pos[0] if fixed_coord is None else self.pos[fixed_coord.value]
        
        lower_bound = -1
        upper_bound = c.SIZE

        # 1) find restrictions in movement due to piece positions
        for coord in range(c.SIZE):
            if coord == fixed:
                continue

            # max below you, min above you
            pos = (None, None)

            if fixed_coord is None:
                pos[0] = coord
                pos[1] = coord
            else:
                pos[fixed_coord.value] = fixed
                pos[1 - fixed_coord.value] = coord
            
            piece = board.get_piece(pos)
            if piece is not None:
                if coord < fixed: # below
                    if self.opponent_piece(piece):
                        lower_bound = max(coord + 1, lower_bound)
                    else:
                        lower_bound = max(coord, lower_bound)
                elif coord > fixed: # above
                    if self.opponent_piece(piece):
                        upper_bound = min(coord + 1, upper_bound)
                    else:
                        upper_bound = min(coord + 1, upper_bound)

        # 2) account for cases where movement is restricted either back or forward
        if lower_bound == -1:
            lower_bound = fixed
        if upper_bound == c.SIZE:
            upper_bound = fixed

        # 3) account for piece movement restrictions (i.e. radius of movement)
        lower_bound = max(fixed - r_neg, lower_bound)
        upper_bound = min(fixed + r_pos, upper_bound)

        # 4) account for board size
        lower_bound = max(lower_bound, 0)
        upper_bound = min(upper_bound, c.SIZE)

        legal = []
        for coord in range(lower_bound, upper_bound + 1):
            if coord == cur_row:
                legal.append(coord)
        return legal

    def vertical_moves(self, board, vert_radius):
        return self._generic_moves(board, vert_radius, fixed_coord=Coord.COL)

    def horizontal_moves(self, board, hor_radius):
        return self._generic_moves(board, hor_radius, fixed_coord=Coord.ROW)

    def diagonal_moevs(self, board, diag_radius):
        return self._generic_moves(board, diag_radius, fixed_coord=None)

    def legal_moves(self, board, radius):
          up_left,   up, up_right, \
             left,          right, \
        down_left, down, down_right = radius

        # no piece has diagonal radial disparity
        assert((up_left, down_right) == (up_right, down_left))

        vertical_legal = self.vertical_moves(board, (up, down))
        horizontal_legal = self.vertical_moves(board, (left, right))
        diagonal_legal = self.vertical_moves(board, (up_left, down_right))

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

        radius = [
            top_left_r, forward, top_right_r,
            0,    0,
            0, 0, 0
        ]
        return self.legal_moves(board, radius)

class Rook(Piece):
    def __init__(self, pos, side):
        super(Rook, self).__init__("R", pos, side)
        
    def legal_moves(self, board):
        radius = [
            0, 8, 0,
            8,    8,
            0, 8, 0
        ]
        return self.legal_moves(board, radius)

class Knight(Piece):
    def __init__(self, pos, side):
        super(Knight, self).__init__("N", pos, side)
        
    def legal_moves(self, board):
        pass

class Bishop(Piece):
    def __init__(self, pos, side):
        super(Bishop, self).__init__("B", pos, side)
        
    def legal_moves(self, board):
        radius = [
            8, 0, 8,
            0,    0,
            8, 0, 8
        ]
        return self.legal_moves(board, radius)

class Queen(Piece):
    def __init__(self, pos, side):
        super(Queen, self).__init__("Q", pos, side)
        
    def legal_moves(self, board):
        radius = [
            8, 8, 8,
            8,    8,
            8, 8, 8
        ]
        return self.legal_moves(board, radius)

class King(Piece):
    def __init__(self, pos, side):
        super(King, self).__init__("K", pos, side)
        
    def legal_moves(self, board):
        radius = [
            1, 1, 1,
            1,    1,
            1, 1, 1
        ]
        return self.legal_moves(board, radius)