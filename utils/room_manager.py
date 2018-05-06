import json
import utils.game as games

class User:
    name = ""
    ready = False
    role = ""

    def __init__(self, user_json):
        self.name = user_json["name"]
        self.ready = user_json["ready"]
        self.role = user_json["role"]


class Room:
    GAME_GO = "go"
    GAME_CHESS = "chess"

    name = ""
    password = False
    deadline = None
    players_ready = False
    game = None
    users = []

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
    date = ""
    duration = 0

    def __init__(self, deadline_json):
        self.date = deadline_json["date"]
        self.duration = deadline_json["duration"]
