import json


class User:
    name = ""
    ready = False
    role = ""

    def __init__(self, user_json):
        self.name = user_json["name"]
        self.ready = user_json["ready"]
        self.role = user_json["role"]


class Room:
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


class Deadline:
    date = ""
    duration = 0

    def __init__(self, deadline_json):
        self.date = deadline_json["date"]
        self.duration = deadline_json["duration"]
