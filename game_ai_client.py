import asyncio
import websocket
import ssl
import json
import threading
import time
import atexit
import utils.room_manager as rm


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

    GAME_GO = "go"
    GAME_CHESS = "chess"

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

    ws = None
    wst = None
    ping_interval = None

    ping_timer_duration = 25

    connected = False

    def __init__(self, on_message):
        self.on_message = on_message
        self.user = None

    def connect(self, url):
        atexit.register(self.disconnect)
        self.ws = websocket.WebSocketApp(url=url)
        self.ws.on_open = self.on_open
        self.ws.on_error = self.on_error
        self.ws.on_message = self.listen
        self.wst = threading.Thread(target=self.ws.run_forever, kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}})
        self.wst.daemon = True
        self.wst.start()

        while not self.connected:
            pass
        self.ping_interval = threading.Thread(target=self.ping_timer)
        self.ping_interval.daemon = True
        self.ping_interval.start()

    def disconnect(self):
        print("Disconnect")
        self.ws.close()
        self.connected = False

    def send(self, message):
        self.ws.send(message)

    def listen(self, ws, message):
        if message == "pong":
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
            self.on_message(self, message)

    def on_error(self, ws, error):
        print("Error {}".format(error))

    def on_open(self, ws):
        self.connected = True

    def ping(self):
        self.send("ping")

    def ping_timer(self):
        while self.connected:
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

    def room_add(self, name, password="", game=GAME_CHESS):
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
