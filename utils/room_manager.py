import json
import utils.game as games

ROLE_WHITE = 1
ROLE_WHITE_STR = "white"

ROLE_BLACK = 2
ROLE_BLACK_STR = "black"

ROLE_SPECTATOR = 3
ROLE_SPECTATOR_STR = "spectator"

CMD_READY = "ready"
CMD_SET_DEADLINE_DUR = "set-deadline-dur"
CMD_SURRENDER = "surrender"
CMD_RESTART = "restart"


class User:

    def __init__(self, user_json):
        self.name = user_json["name"]
        self.ready = user_json["ready"]
        self.role = user_json["role"]

        if self.role == ROLE_BLACK_STR:
            self.role_id = ROLE_BLACK
        elif self.role == ROLE_WHITE_STR:
            self.role_id = ROLE_WHITE
        else:
            self.role_id = ROLE_SPECTATOR


class Room:
    GAME_GO = "go"
    GAME_CHESS = "chess"

    def __init__(self, room_json):
        self.name = room_json["name"]
        self.password = room_json["password"]
        self.deadline = Deadline(room_json["deadline"])
        self.players_ready = room_json["players_ready"]
        self.game = None
        self.users = []
        for user_json in room_json["users"]:
            self.users.append(User(user_json))

        if room_json["game"]["name"] == games.GAME_CHESS:
            self.game = games.Chess(room_json["game"])
        else:
            self.game = games.Go(room_json["game"])


class Deadline:

    def __init__(self, deadline_json):
        self.date = deadline_json["date"]
        self.duration = deadline_json["duration"]
