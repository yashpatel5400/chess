class Piece:
    def __init__(self, name, pos, side):
        self.name = name
        self.pos = pos
        self.side = side

    def __str__(self):
        START_CHAR = 64
        row, col = self.pos
        return f"{self.side.value}{self.name}({chr(START_CHAR + col + 1)}{row + 1})"

    def legal_moves(self, board):
        pass

class Pawn(Piece):
    def __init__(self, pos, side):
        super(Pawn, self).__init__("P", pos, side)
        self.previously_moved = False

    def legal_moves(self, board):
        pass

class Rook(Piece):
    def __init__(self, pos, side):
        super(Rook, self).__init__("R", pos, side)
        
    def legal_moves(self, board):
        pass

class Knight(Piece):
    def __init__(self, pos, side):
        super(Knight, self).__init__("N", pos, side)
        
    def legal_moves(self, board):
        pass

class Bishop(Piece):
    def __init__(self, pos, side):
        super(Bishop, self).__init__("B", pos, side)
        
    def legal_moves(self, board):
        pass

class Queen(Piece):
    def __init__(self, pos, side):
        super(Queen, self).__init__("Q", pos, side)
        
    def legal_moves(self, board):
        pass

class King(Piece):
    def __init__(self, pos, side):
        super(King, self).__init__("K", pos, side)
        
    def legal_moves(self, board):
        pass