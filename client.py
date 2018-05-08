import game_ai_client as aic
import json
import utils.game as game
import utils.room_manager as room_manager
import utils.game_as.chess as chess_as
import random
import time


def on_message(obj, msg):
    msg_json = json.loads(msg)
    method = msg_json[aic.GameAIClient.METHOD]
    print(method)
    if method == aic.GameAIClient.METHOD_ERROR:
        print(msg)

    if method == aic.GameAIClient.METHOD_ROOM_JOIN or method == aic.GameAIClient.METHOD_ROOM_ADD:
        room = room_manager.Room(msg_json["data"])

        role_black_taken = False
        role_white_taken = False
        for user in room.users:
            if user.role == aic.GameAIClient.ROLE_WHITE_STR:
                role_white_taken = True
            if user.role == aic.GameAIClient.ROLE_BLACK_STR:
                role_black_taken = True

        if not role_black_taken:
            obj.role_change(aic.GameAIClient.ROLE_BLACK)
        elif not role_white_taken:
            obj.role_change(aic.GameAIClient.ROLE_WHITE)

    if msg_json[aic.GameAIClient.METHOD] == aic.GameAIClient.METHOD_ROOM_UPDATE:
        time.sleep(1)
        room = room_manager.Room(msg_json["data"])

        if obj.user.role != aic.GameAIClient.ROLE_SPECTATOR:
            if not obj.user.ready:
                obj.room_command(aic.GameAIClient.CMD_READY)

        if room.players_ready:
            field = chess_as.get_field(room.game)
            moves = chess_as.get_valid_moves(field, room.game.turn)
            print(str(len(moves)) + " Possible Moves")

            move = moves[random.randint(0, len(moves)-1)][0]
            print("Selected Move: " + move)
            obj.game_move(move)


if __name__ == "__main__":
    print("API Client 1.0")

    client = aic.GameAIClient(on_message)
    client.connect("wss://vg-development.de:8900/game")
    client.login("Bot-" + str(random.randint(0, 999999)))
    client.room_add("BotRoom " + str(random.randint(0, 999999)))

    while client.connected:
        time.sleep(10)



