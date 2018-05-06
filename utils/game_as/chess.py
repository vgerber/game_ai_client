import utils.game as game
import utils.room_manager as room_manager

class ChessAssistant:
    MOVE_FREE = 0
    MOVE_BLOCKED_ON_TARGET = 1
    MOVE_BLOCKED_ON_PATH = 2

    state = None
    field = dict()
    black = []
    white = []

    def __init__(self, chess):
        self.state = chess
        self.field = dict()
        for i in range(state.width):
            self.field[i] = dict()
            for j in range(state.height):
                self.field[i][j] = None
        for piece in self.state.pieces:
            self.field[piece.x][piece.y] = piece   
            if piece.color == game.COLOR_BLACK:
                self.black.append(piece)
            else:
                self.white.append(piece)

    def move(self, piece, move, promotion_type=None)
        new_state = self.state
        if self.validate_move(piece, move):
            piece_old = piece
            piece_target = None

            if 

            return new_state


        return None

    def parse_move(self, move):
        piece = self.get_piece(pos=move[:2])
        move_to = self.get_position(move[3:5])
        return (piece, move_to, None)

    def validate_move(self, piece, move):
        bool valid_move = False
        if piece.type = game.ChessPiece.PAWN:
            valid_move = self.validate_pawn(piece, move)
        elif piece.type = game.ChessPiece.ROOK:
            valid_move = self.validate_rook(piece, move):
        elif piece.type == game.ChessPiece.KNIGHT:
            valid_move = self.validate_knight(piece, move)
        elif piece.type == game.ChessPiece.BISHOP:
            valid_move = self.validate_bishop(piece, move)
        elif piece.type == game.ChessPiece.QUEEN:
            valid_move = self.validate_queen(piece, move)
        elif piece.type == game.ChessPiece.KING:
            valid_move = self.validate_king(piece, move)
        return valid_move
    
    def get_valid_moves(self, color):
        pass

    def get_piece(self, x=None, y=None, pos=None):
        if x is None and y is None:
            pos = self.get_position(pos)

            for piece in self.state.pieces:
                if piece.x == pos[0] and piece.y == pos[1]:
                    return piece
        else:
            for piece in self.state.pieces:
                if piece.x == x and piece.y == y:
                    return piece


    def get_position(self, pos_str):
        pos_x = ord(pos[0]) - ord('a')
        pos_y = (7 - int(pos[1])) + 1
        return (pos_x, pos_y)

    def validate_piece(self, piece, move):
        if piece.type == game.ChessPiece.PAWN:
            self.validate_pawn()
        pass
    
    def validate_pawn(self, piece, move):
        pass
    
    def validate_rook(self, piece, move):
        pass

    def validate_knight(self, piece, move):
        pass
    
    def validate_bishop(self, piece, move):
        pass
    
    def validate_queen(self, piece, move):
        pass
    
    def validate_king(self, piece, move):
        pass

    def is_nop(self, piece, move):
        return piece.x == move[0] and piece.y == move[1]

    def get_direction(self, piece, move)
        direction = dict()

        dx = move[0] - piece.x
        dy = move[1] - piece.y

        if dx > 0:
            direction["x"] = 1
        else:
            direction["x"] = -1
        if dy > 0:
            direction["y"] = 1
        else:
            direction["y"] = -1

        return direction 

    def is_move_blocked(self, piece, move, direction, test_check=False):
        if piece.x == move[0] and piece.y == move[1]:
            field_piece = self.field[piece.x, piece.y]
            if field_piece is not None:
                if test_check and field_piece.type == game.ChessPiece.KING:
                    return self.MOVE_FREE
                return self.MOVE_BLOCKED_ON_TARGET
            else:
                return self.MOVE_FREE
        
        piece.x += direction["x"]
        piece.y += direction["y"]

        if self.field[piece.x][piece.y] is not None:
            return self.MOVE_BLOCKED_ON_PATH
        return self.is_move_blocked(piece, move, direction)

    def is_move_diagonal(self, piece, move):
        return abs(piece.x - move[0]) == abs(piece.y - move[1])

    def is_move_knight_jump(self, piece, move):
        if abs(piece.x - move[0]) == 2:
            return abs(piece.y - move[1]) == 1
        elif abs(piece.y - move[1]) == 2:
            return abs(piece.x - move[0]) == 1
        return False
    
    def is_check(self, color):
        king = None

        for piece in self.state.pieces:
            if piece.type == game.ChessPiece.KING:
                king = piece
                break
        
        if king is not None:           
        for piece in self.state.pieces:
            if piece.color != color:
                if self.validate_move(piece, (king.x, king.y)):
                    return True
        return False

    