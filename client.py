import game_ai_client as aic
import json
import utils.game as game
import utils.room_manager as room_manager
import utils.game_as.chess as chess_as
import random
import time


def on_message(msg):

    msg_json = json.loads(msg)

    print(msg_json[aic.GameAIClient.METHOD])
    if msg_json[aic.GameAIClient.METHOD] == aic.GameAIClient.METHOD_ROOM_ADD:
        room = room_manager.Room(msg_json["data"])
        field = chess_as.get_field(room.game)
        # print(field[1])

        moves = chess_as.get_valid_moves(field, room.game.turn)
        print(len(moves))
        print(room)


if __name__ == "__main__":
    print("API Client 1.0")

    client = aic.GameAIClient(on_message)
    client.connect("wss://vg-development.de:8900/game")
    client.login("Test")#str(random.randint(0, 999999)))
    client.room_all()
    client.room_add("BotRoom-" + str(random.randint(0, 999999)))

    time.sleep(120)



