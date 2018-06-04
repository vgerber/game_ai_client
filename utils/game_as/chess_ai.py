import utils.game_as.chess as chess
import utils.game as game_struct
import copy


def heuristic(game, piece, color):
    value = 0
    if piece.type == game_struct.ChessPiece.PAWN:
        value = 1
    elif piece.type == game_struct.ChessPiece.ROOK:
        value = 2
    elif piece.type == game_struct.ChessPiece.KNIGHT:
        value = 3
    elif piece.type == game_struct.ChessPiece.BISHOP:
        value = 5
    elif piece.type == game_struct.ChessPiece.QUEEN:
        value = 8
    elif piece.type == game_struct.ChessPiece.KING:
        value = 9
    if color != piece.color:
        value *= -1
    return value


def evaluate_game(game, color, field=None):
    value = 0
    if field is None:
        field = chess.get_field(game)
    for x in range(game.width):
        for y in range(game.height):
            piece = field[x][y]
            if piece is not None:
                value += heuristic(game, piece, color)
    return value


def min_max(game, depth):
    return mm_max(game, chess.get_field(game), depth)


def mm_min(game, field, depth):
    min_turn = (game.turn + 1) % 2
    if depth == 0:
        return None

    depth = copy.copy(depth)
    moves = chess.get_valid_moves(field, min_turn)
    values = []

    for move in moves:
        piece, target_move, promotion = chess.parse_move(field, move[0])
        next_field = chess.move(field, piece, target_move)
        value = evaluate_game(game, game.turn, next_field)
        max_result = mm_max(game, next_field, depth-1)
        if max_result is not None:
            value += max_result[0]
        values.append((value, move[0]))

    min_val = float("inf")
    min_i = -1
    for i, value in enumerate(values):
        if value[0] < min_val:
            min_val = value[0]
            min_i = i
    if min_i > -1:
        return values[min_i]
    else:
        return None


def mm_max(game, field, depth):
    if depth == 0:
        return None
    depth = copy.copy(depth)
    moves = chess.get_valid_moves(field, game.turn)
    values = []

    for move in moves:
        piece, target_move, promotion = chess.parse_move(field, move[0])
        next_field = chess.move(field, piece, target_move)
        value = evaluate_game(game, game.turn, next_field)

        min_result = mm_min(game, next_field, depth)
        if min_result is not None:
            value += min_result[0]

        values.append((value, move[0]))

    max_val = float("-inf")
    max_i = -1
    for i, value in enumerate(values):
        if value[0] > max_val:
            max_val = value[0]
            max_i = i
    if max_i > -1:
        return values[max_i]
    else:
        return None

