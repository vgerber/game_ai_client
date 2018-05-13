import utils.game as game
import utils.room_manager as room_manager
import copy

MOVE_FREE = 0
MOVE_BLOCKED_ON_TARGET = 1
MOVE_BLOCKED_ON_PATH = 2


def print_field(field):
    for y in range(8):
        for x in range(8):
            if field[x][y] is None:
                print("-", end='')
            else:
                print("{}".format(field[x][y]), end='')
        print("")


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
    new_field = copy.deepcopy(field)
    piece_cpy = copy.copy(piece)
    if validate_piece(field, piece, target_move):
        new_field[piece_cpy.x][piece_cpy.y] = None

        piece_cpy.x = target_move[0]
        piece_cpy.y = target_move[1]
        piece_cpy.move_count += 1
        new_field[piece_cpy.x][piece_cpy.y] = piece_cpy
        if is_check(new_field, piece.color):
            return None
        return new_field
    return None


def parse_move(field, target_move):
    piece = get_piece(field=field, pos=target_move[:2])
    move_to = get_position(target_move[3:5])
    return piece, move_to, None


def get_move_str(piece, target_move):
    from_str = "{}{}".format(chr(ord('a') + piece.x), (7-piece.y)+1)
    to_str = "{}{}".format(chr(ord('a') + target_move[0]), (7-target_move[1])+1)
    return from_str + "-" + to_str


def get_valid_moves(field, color):
    moves = []
    for x in range(8):
        for y in range(8):
            piece = field[x][y]
            if piece is not None and piece.color == color:
                for move_x in range(8):
                    for move_y in range(8):
                        state = move(field, piece, (move_x, move_y))
                        if state is not None:
                            move_str = get_move_str(piece, (move_x, move_y))
                            moves.append((move_str, copy.deepcopy(state)))
    return moves


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


def validate_piece(field, piece, target_move, ignore_king=False):
    valid_move = False
    if piece.type == game.ChessPiece.PAWN:
        valid_move = validate_pawn(field, piece, target_move, ignore_king)
    elif piece.type == game.ChessPiece.ROOK:
        valid_move = validate_rook(field, piece, target_move, ignore_king)
    elif piece.type == game.ChessPiece.KNIGHT:
        valid_move = validate_knight(field, piece, target_move, ignore_king)
    elif piece.type == game.ChessPiece.BISHOP:
        valid_move = validate_bishop(field, piece, target_move, ignore_king)
    elif piece.type == game.ChessPiece.QUEEN:
        valid_move = validate_queen(field, piece, target_move, ignore_king)
    elif piece.type == game.ChessPiece.KING:
        valid_move = validate_king(field, piece, target_move, ignore_king)
    return valid_move


def validate_pawn(field, piece, target_move, ignore_king=False):
    if is_nop(piece, target_move):
        return False
    if not is_move_in_bounds(target_move):
        return False

    dx = abs(piece.x - target_move[0])
    dy = abs(piece.y - target_move[1])
    direction = get_direction(piece, target_move)

    if piece.color == game.COLOR_BLACK:
        if direction["y"] <= 0:
            return False
    else:
        if direction["y"] >= 0:
            return False

    if dx == 0:
        if dy == 1 or (dy == 2 and piece.move_count == 0):
            return is_move_blocked(field, piece, target_move, direction, ignore_king) == MOVE_FREE
    if dx == 1 and dy == 1:
        expected_result = MOVE_BLOCKED_ON_TARGET
        if ignore_king:
            expected_result = MOVE_FREE
        return is_move_blocked(field, piece, target_move, direction, ignore_king) == expected_result

    return False


def validate_rook(field, piece, target_move, ignore_king=False):
    if is_nop(piece, target_move):
        return False
    if not is_move_in_bounds(target_move):
        return False
    direction = get_direction(piece, target_move)

    if is_move_linear(piece, target_move):
        return is_move_blocked(field, piece, target_move, direction, ignore_king) != MOVE_BLOCKED_ON_PATH

    return False


def validate_knight(field, piece, target_move, ignore_king=False):
    if is_nop(piece, target_move):
        return False
    if not is_move_in_bounds(target_move):
        return False

    if is_move_knight_jump(piece, target_move):
        target_piece = field[target_move[0]][target_move[1]]

        if ignore_king and target_piece.type == game.ChessPiece.KING:
            return True

        return (target_piece is None) or (target_piece.color != piece.color)

    return False


def validate_bishop(field, piece, target_move, ignore_king=False):
    if is_nop(piece, target_move):
        return False
    if not is_move_in_bounds(target_move):
        return False
    direction = get_direction(piece, target_move)

    if is_move_diagonal(piece, target_move):
        return is_move_blocked(field, piece, target_move, direction, ignore_king) != MOVE_BLOCKED_ON_PATH

    return False


def validate_queen(field, piece, target_move, ignore_king=False):
    if is_nop(piece, target_move):
        return False
    if not is_move_in_bounds(target_move):
        return False
    direction = get_direction(piece, target_move)

    if is_move_diagonal(piece, target_move) or is_move_linear(piece, target_move):
        return is_move_blocked(field, piece, target_move, direction, ignore_king) != MOVE_BLOCKED_ON_PATH

    return False


def validate_king(field, piece, target_move, ignore_king=False):
    if is_nop(piece, target_move):
        return False
    if not is_move_in_bounds(target_move):
        return False
    dx = abs(piece.x - target_move[0])
    dy = abs(piece.y - target_move[1])
    direction = get_direction(piece, target_move)

    if dx <= 1 and dy <= 1:
        return is_move_blocked(field, piece, target_move, direction, ignore_king) != MOVE_BLOCKED_ON_PATH

    return False


def is_nop(piece, target_move):
    return piece.x == target_move[0] and piece.y == target_move[1]


def is_move_in_bounds(target_move):
    return 0 <= target_move[0] < 8 and 0 <= target_move[1] < 8


def get_direction(piece, target_move):
    direction = dict()

    dx = target_move[0] - piece.x
    dy = target_move[1] - piece.y

    if dx > 0:
        direction["x"] = 1
    elif dx == 0:
        direction["x"] = 0
    else:
        direction["x"] = -1
    if dy > 0:
        direction["y"] = 1
    elif dy == 0:
        direction["y"] = 0
    else:
        direction["y"] = -1

    return direction


def is_move_blocked(field, piece, target_move, direction, test_check=False):
    field = copy.deepcopy(field)
    piece_cpy = copy.copy(piece)

    piece_cpy.x += direction["x"]
    piece_cpy.y += direction["y"]

    if piece_cpy.x == target_move[0] and piece_cpy.y == target_move[1]:
        field_piece = field[piece_cpy.x][piece_cpy.y]
        # test if field is blocked by piece
        if field_piece is not None:
            # move is free if testing for check
            if test_check and field_piece.type == game.ChessPiece.KING:
                return MOVE_FREE
            # return blocked by ally when both pieces have the same color
            if piece_cpy.color == field_piece.color:
                return MOVE_BLOCKED_ON_PATH
            return MOVE_BLOCKED_ON_TARGET
        else:
            return MOVE_FREE

    if field[piece_cpy.x][piece_cpy.y] is not None:
        return MOVE_BLOCKED_ON_PATH
    return is_move_blocked(field, piece_cpy, target_move, direction, test_check)


def is_move_diagonal(piece, target_move):
    return abs(piece.x - target_move[0]) == abs(piece.y - target_move[1])


def is_move_knight_jump(piece, target_move):
    if abs(piece.x - target_move[0]) == 2:
        return abs(piece.y - target_move[1]) == 1
    elif abs(piece.y - target_move[1]) == 2:
        return abs(piece.x - target_move[0]) == 1
    return False


def is_move_linear(piece, target_move):
    dx = abs(piece.x - target_move[0])
    dy = abs(piece.y - target_move[1])
    return (dx == 0 and dy != 0) or (dx != 0 and dy == 0)


def is_check(field, color):
    king = None

    for x in range(8):
        for y in range(8):
            piece = field[x][y]
            if piece is not None and color == piece.color and piece.type == game.ChessPiece.KING:
                king = piece
                break

    if king is not None:
        for x in range(8):
            for y in range(8):
                piece = field[x][y]
                if piece is not None and piece.color != color:
                    if validate_piece(field, piece, (king.x, king.y), ignore_king=True):
                        return True
    return False


def is_check_mate(field, color):
    king = None

    for x in range(8):
        for y in range(8):
            piece = field[x][y]
            if piece is not None and color == piece.color and piece.type == game.ChessPiece.KING:
                king = piece
                break

    if king is not None:
        # check if king can move
        for x in range(-1, 2):
            for y in range(-1, 2):
                if move(field, king, (king.x + x, king.y + y)) is not None:
                    return False

        for x in range(8):
            for y in range(8):
                piece = field[x][y]
                if piece is not None and piece.color == color:
                    for move_x in range(8):
                        for move_y in range(8):
                            state = move(field, piece, (move_x, move_y))
                            if state is not None:
                                return False
        return True
    return False


def is_stale_mate(field, color):
    if not is_check(field, color):
        king = None
        for x in range(8):
            for y in range(8):
                piece = field[x][y]
                if piece is not None and piece.color == color and piece.type == game.ChessPiece.KING:
                    king = piece
                    break
        # test if king can move
        for x in range(-1, 2):
            for y in range(-1, 2):
                if move(field, king, (king.x + x, king.y + y)) is not None:
                    return False
        # test if any piece from own color can move
        for x in range(8):
            for y in range(8):
                piece = field[x][y]
                if piece is not None and piece.color == color and piece.type != game.ChessPiece.KING:
                    for move_x in range(8):
                        for move_y in range(8):
                            state = move(field, piece, (move_x, move_y))
                            if state is not None:
                                return False

        return True
    return False

