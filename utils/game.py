import json

COLOR_EMPTY = -1
COLOR_WHITE = 0
COLOR_BLACK = 1


class GoPiece:
    color = COLOR_EMPTY
    x = 0
    y = 0

    def __init__(self, json_go_piece):
        self.color = json_go_piece["color"]
        self.x = json_go_piece["x"]
        self.y = json_go_piece["y"]


class GoStatePlayer:
    pass_turn = False
    captured = 0
    score = 0

    def __init__(self, json_player_state):
        self.pass_turn = json_player_state["pass"]
        self.captured = json_player_state["captured"]
        self.score = json_player_state["score"]


class GoState:
    STATE_OK = 1
    STATE_ERROR = 0
    STATE_WHITE_WON = 20
    STATE_BLACK_WON = 21
    STATE_JIGO = 3

    game_state = 0
    black = None
    white = None

    def __init__(self, json_state):
        self.game_state = json_state["game_state"]
        self.black = GoStatePlayer(json_state["black"])
        self.white = GoStatePlayer(json_state["white"])


class Go:
    CMD_PASS = "pass"

    name = ""
    count = 0
    turn = COLOR_EMPTY
    width = 0
    height = 0
    last_move = ""
    pieces = []
    state = None

    def __init__(self, json_go):
        self.name = json_go["name"]
        self.count = json_go["count"]
        self.turn = json_go["turn"]
        self.width = json_go["width"]
        self.height = json_go["height"]
        self.last_move = json_go["last_move"]

        self.pieces = []
        for piece in json_go["pieces"]:
            self.pieces.append(GoPiece(piece))

        self.state = GoState(json_go["state"])


class ChessPiece:
    PAWN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    QUEEN = 5
    KING = 6

    color = COLOR_EMPTY
    x = 0
    y = 0
    type = PAWN
    out = False
    move_count = 0


    def __init__(self, json_piece):
        self.color = json_piece["color"]
        self.x = json_piece["x"]
        self.y = json_piece["y"]
        self.type = json_piece["type"]
        self.out = json_piece["out"]
        self.move_count = json_piece["move_count"]


class ChessState:
    STATE_OK = 1
    STATE_WHITE_WON = 4
    STATE_BLACK_WON = 3
    STATE_REMIS = 2

    PLAYER_OK = 1
    PLAYER_CHECK = 0

    game_state = 0
    black = 0
    white = 0

    def __init__(self, json_state):
        self.game_state = json_state["game_state"]
        self.black = json_state["black"]
        self.white = json_state["white"]


class Chess:
    name = ""
    count = 0
    turn = COLOR_EMPTY
    width = 0
    height = 0
    last_move = ""
    pieces = []
    state = None

    def __init__(self, json_go):
        self.name = json_go["name"]
        self.count = json_go["count"]
        self.turn = json_go["turn"]
        self.width = json_go["width"]
        self.height = json_go["height"]
        self.last_move = json_go["last_move"]

        self.pieces = []
        for piece in json_go["pieces"]:
            self.pieces.append(ChessPiece(piece))

        self.state = ChessState(json_go["state"])
