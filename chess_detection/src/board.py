import typing as t


PieceType = int
ColorType = int


class Pieces:
    mask: int = 0b00111

    BLANK: PieceType = 0
    PAWN: PieceType = 1
    ROOK: PieceType = 2
    KNIGHT: PieceType = 3
    BISHOP: PieceType = 4
    QUEEN: PieceType = 5
    KING: PieceType = 6


class Colors:
    mask: int = 0b11000

    WHITE: ColorType = 8
    BLACK: ColorType = 16


class Board:
    """
    Board is always represented from `eigth rank` to `first rank`, and `eight file` to
    `first file`, as per FEN convention.
    """

    def __init__(
        self,
        piece_placements: t.List[t.List[int]],
        active_color: ColorType,
    ):
        self.piece_placements = piece_placements
        self.active_color = active_color

    @staticmethod
    def decode_fen_square(sq: str) -> int:
        sq_color = Colors.BLACK if sq.islower() else Colors.WHITE

        sq = sq.lower()
        if sq == "p":
            sq_piece = Pieces.PAWN
        elif sq == "r":
            sq_piece = Pieces.ROOK
        elif sq == "n":
            sq_piece = Pieces.KNIGHT
        elif sq == "b":
            sq_piece = Pieces.BISHOP
        elif sq == "q":
            sq = Pieces.QUEEN
        elif sq == "k":
            sq_piece = Pieces.KING

        return sq_color | sq_piece

    @staticmethod
    def encode_fen_square(sq: int) -> str:
        sq_color = sq & Colors.mask
        sq_piece = sq & Pieces.mask
        if sq_piece == Pieces.PAWN:
            sq = "p"
        elif sq_piece == Pieces.ROOK:
            sq = "r"
        elif sq_piece == Pieces.KNIGHT:
            sq = "n"
        elif sq_piece == Pieces.BISHOP:
            sq = "b"
        elif sq_piece == Pieces.QUEEN:
            sq = "q"
        elif sq_piece == Pieces.KING:
            sq = "k"

        return sq if (sq_color == Colors.BLACK) else sq.upper()

    @classmethod
    def from_fen(cls, fen: str):
        """
        Converts `FEN` representation into an 8x8 array representiting the chess
        board. Analogous to the FEN representation, the array representation also
        starts from eight rank and eight file.

        We use a modified version of FEN where we only consider the first two fields:
        - `Piece Placement`
        - `Active Color`

        More on FEN: https://www.chess.com/terms/fen-chess
        """
        piece_placements_fen, active_color_fen = fen.split(" ")
        piece_placements_fen = piece_placements_fen.split("/")
        active_color = Colors.BLACK if active_color_fen == "b" else Colors.WHITE

        piece_placements: t.List[t.List[PieceType]] = list()

        for rank_fen in piece_placements_fen:
            rank = list()
            for square in rank_fen:
                if square.isnumeric():
                    rank += [Pieces.BLANK] * int(square)
                else:
                    rank.append(cls.decode_fen_square(square))
            piece_placements.append(rank)

        return cls(piece_placements, active_color)

    def fen(self) -> str:
        active_color_fen = "b" if self.active_color == Colors.BLACK else "w"

        piece_placements_fen: str = ""
        for rank in self.piece_placements:
            rank_fen: str = ""
            for square in rank:
                if square == Pieces.BLANK:
                    if rank_fen and rank_fen[-1].isnumeric():
                        rank_fen = rank_fen[:-1] + str(int(rank_fen[-1]) + 1)
                    else:
                        rank_fen += "1"
                else:
                    rank_fen += self.encode_fen_square(square)
            piece_placements_fen += ("/" if piece_placements_fen else "") + rank_fen

        fen = piece_placements_fen + " " + active_color_fen
        return fen
