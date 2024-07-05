from chess.Pieces import Piece


class Move:
    def __init__(self, piece_square: list[int], destination: list[int], captured_storage: Piece, promotion: Piece,
                 eped: bool):
        self.piece_square = piece_square
        self.destination = destination
        self.captured_storage = captured_storage
        self.promotion = promotion
        self.eped = eped
