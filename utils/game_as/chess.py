import utils.game as game
import utils.room_manager as room_manager

MOVE_FREE = 0
MOVE_BLOCKED_ON_TARGET = 1
MOVE_BLOCKED_ON_PATH = 2


def get_field(chess):
    field = dict()
    for i in range(chess.width):
        field[i] = dict()
        for j in range(chess.height):
            field[i][j] = None
    for piece in chess.pieces:
        if not piece.out:
            field[piece.x][piece.y] = piece
    return field


def move(field, piece, target_move, promotion_type=None):
    new_field = field
    if validate_piece(piece, target_move):
        piece_old = piece
        piece_target_old = None
        piece_target = field[target_move[0]][target_move[1]]

        piece.x = target_move[0]
        piece.y = target_move[1]
        piece.move_count += 1
        if piece_target is not None:
            piece_target_old = piece_target
            new_field[piece_old.x][piece_old.y] = None
            new_field[piece.x][piece.y] = piece
            piece_target.out = True
            piece_target.x = -1
            piece_target.y = -1

        return new_field
    return None


def parse_move(field, target_move):
    piece = get_piece(field=field, pos=target_move[:2])
    move_to = get_position(target_move[3:5])
    return piece, move_to, None


def get_valid_moves(self, color):
    pass


def get_piece(field, x=None, y=None, pos=None):
    if x is None and y is None:
        pos = get_position(pos)

        for x in range(8):
            for y in range(8):
                piece = field[x][y]
                if piece.x == pos[0] and piece.y == pos[1]:
                    return piece
    else:
        for x in range(8):
            for y in range(8):
                piece = field[x][y]
                if piece.x == x and piece.y == y:
                    return piece


def get_position(pos_str):
    pos_x = ord(pos_str[0]) - ord('a')
    pos_y = (7 - int(pos_str[1])) + 1
    return pos_x, pos_y


def validate_piece(piece, target_move):
    valid_move = False
    if piece.type == game.ChessPiece.PAWN:
        valid_move = validate_pawn(piece, target_move)
    elif piece.type == game.ChessPiece.ROOK:
        valid_move = validate_rook(piece, target_move)
    elif piece.type == game.ChessPiece.KNIGHT:
        valid_move = validate_knight(piece, target_move)
    elif piece.type == game.ChessPiece.BISHOP:
        valid_move = validate_bishop(piece, target_move)
    elif piece.type == game.ChessPiece.QUEEN:
        valid_move = validate_queen(piece, target_move)
    elif piece.type == game.ChessPiece.KING:
        valid_move = validate_king(piece, target_move)
    return valid_move


def validate_pawn(piece, target_move):
    return False


def validate_rook(piece, target_move):
    return False


def validate_knight(piece, target_move):
    return False


def validate_bishop( piece, target_move):
    return False


def validate_queen(piece, target_move):
    return False


def validate_king(piece, target_move):
    return False


def is_nop(piece, target_move):
    return piece.x == target_move[0] and piece.y == target_move[1]


def get_direction(piece, target_move):
    direction = dict()

    dx = target_move[0] - piece.x
    dy = target_move[1] - piece.y

    if dx > 0:
        direction["x"] = 1
    else:
        direction["x"] = -1
    if dy > 0:
        direction["y"] = 1
    else:
        direction["y"] = -1

    return direction


def is_move_blocked(field, piece, move, direction, test_check=False):
    if piece.x == move[0] and piece.y == move[1]:
        field_piece = field[piece.x, piece.y]
        if field_piece is not None:
            if test_check and field_piece.type == game.ChessPiece.KING:
                return MOVE_FREE
            return MOVE_BLOCKED_ON_TARGET
        else:
            return MOVE_FREE

    piece.x += direction["x"]
    piece.y += direction["y"]

    if field[piece.x][piece.y] is not None:
        return MOVE_BLOCKED_ON_PATH
    return is_move_blocked(piece, move, direction)


def is_move_diagonal(piece, target_move):
    return abs(piece.x - target_move[0]) == abs(piece.y - target_move[1])


def is_move_knight_jump(piece, target_move):
    if abs(piece.x - target_move[0]) == 2:
        return abs(piece.y - target_move[1]) == 1
    elif abs(piece.y - target_move[1]) == 2:
        return abs(piece.x - target_move[0]) == 1
    return False


def is_check(color, field):
    king = None

    for x in range(8):
        for y in range(8):
            piece = field[x][y]
            if color == piece.color and piece.type == game.ChessPiece.KING:
                king = piece
                break

    if king is not None:
        for x in range(8):
            for y in range(8):
                piece = field[x][y]
                if piece.color != color:
                    if validate_piece(piece, (king.x, king.y)):
                        return True
    return False


def is_check_mate(field, color):
    king = None

    for x in range(8):
        for y in range(8):
            piece = field[x][y]
            if color == piece.color and piece.type == game.ChessPiece.KING:
                king = piece
                break

    if king is not None:
        #check possible king moves
        pass

    return False

