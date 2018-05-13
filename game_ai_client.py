import asyncio
import websocket
import ssl
import json
import threading
import time
import atexit
import utils.room_manager as rm
import utils.game as games


class GameAIClient:
    METHOD = "method"
    METHOD_INIT = "init"
    METHOD_ERROR = "error"
    METHOD_AUTH_GUEST = "auth-guest"
    METHOD_AUTH_LOGOUT = "auth-logout"
    METHOD_ROOM_ALL = "room-all"
    METHOD_ROOM_ADD = "room-add"
    METHOD_ROOM_JOIN = "room-join"
    METHOD_ROOM_LEAVE = "room-leave"
    METHOD_ROOM_UPDATE = "room-update"
    METHOD_ROOM_COMMAND = "room-command"
    METHOD_ROLE_CHANGE = "role-change"
    METHOD_GAME_MOVE = "game-move"

    ping_interval = None

    ping_timer_duration = 25

    def __init__(self):
        self.user = None

    def connect(self, url):
        atexit.register(self.disconnect)
        self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        self.ws.connect(url)

        self.ping_interval = threading.Thread(target=self.ping_timer)
        self.ping_interval.daemon = True
        self.ping_interval.start()

    def disconnect(self):
        print("Disconnect")
        self.ws.close()

    def send(self, message):
        self.ws.send(message)

    def receive(self):
        message = self.ws.recv()
        if message is None:
            return None
        if message == "pong" or message == "ping":
            pass
        else:
            msg_json = json.loads(message)
            method = msg_json[self.METHOD]
            if method == self.METHOD_AUTH_GUEST:
                self.user = rm.User(msg_json["data"])
            if method == self.METHOD_ROOM_UPDATE:
                room = rm.Room(msg_json["data"])
                for user in room.users:
                    if user.name == self.user.name:
                        self.user = user
                        break
            return message

    def ping(self):
        self.send("ping")

    def ping_timer(self):
        while self.ws.connected:
            self.ping()
            time.sleep(self.ping_timer_duration)

    def login(self, name):
        msg = dict()
        msg["method"] = self.METHOD_AUTH_GUEST
        msg["data"] = dict()
        msg["data"]["username"] = name
        self.send(json.dumps(msg))

    def logout(self):
        msg = dict()
        msg["method"] = self.METHOD_AUTH_LOGOUT
        msg["data"] = dict()

    def room_all(self):
        msg = dict()
        msg["method"] = self.METHOD_ROOM_ALL
        msg["data"] = dict()
        self.send(json.dumps(msg))

    def room_add(self, name, password="", game=games.GAME_CHESS):
        msg = dict()
        msg["method"] = self.METHOD_ROOM_ADD
        msg["data"] = dict()
        msg["data"]["name"] = name
        msg["data"]["password"] = password
        msg["data"]["game"] = game
        self.send(json.dumps(msg))

    def room_join(self, room_name, password=""):
        msg = dict()
        msg["method"] = self.METHOD_ROOM_JOIN
        msg["data"] = dict()
        msg["data"]["room"] = room_name
        msg["data"]["password"] = password
        self.send(json.dumps(msg))

    def room_leave(self):
        msg = dict()
        msg["method"] = self.METHOD_ROOM_LEAVE
        msg["data"] = dict()
        self.send(json.dumps(msg))

    def room_command(self, command):
        msg = dict()
        msg["method"] = self.METHOD_ROOM_COMMAND
        msg["data"] = dict()
        msg["data"]["command"] = command
        self.send(json.dumps(msg))

    def role_change(self, role):
        msg = dict()
        msg["method"] = self.METHOD_ROLE_CHANGE
        msg["data"] = dict()
        msg["data"]["role"] = role
        self.send(json.dumps(msg))

    def game_move(self, move):
        msg = dict()
        msg["method"] = self.METHOD_GAME_MOVE
        msg["data"] = dict()
        msg["data"]["move"] = move
        self.send(json.dumps(msg))
