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
    # print(method)
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
        room = room_manager.Room(msg_json["data"])

        if obj.user.role != aic.GameAIClient.ROLE_SPECTATOR:
            if not obj.user.ready:
                obj.room_command(aic.GameAIClient.CMD_READY)

        if room.players_ready:
            can_play = False
            if obj.user.role == aic.GameAIClient.ROLE_BLACK_STR:
                can_play = room.game.turn == game.COLOR_BLACK
            elif obj.user.role == aic.GameAIClient.ROLE_WHITE_STR:
                can_play = room.game.turn == game.COLOR_WHITE

            if can_play and room.game.state.game_state == game.ChessState.STATE_OK:
                field = chess_as.get_field(room.game)
                moves = chess_as.get_valid_moves(field, room.game.turn)

                move = moves[random.randint(0, len(moves)-1)][0]
                print("{} Moves -> {}".format(len(moves), move))
                obj.game_move(move)
        if obj.user.role == aic.GameAIClient.ROLE_BLACK_STR and room.game.state.game_state != game.ChessState.STATE_OK:
            obj.room_command(aic.GameAIClient.CMD_RESTART)


if __name__ == "__main__":
    print("API Client 1.0")

    client = aic.GameAIClient(on_message)
    client.connect("ws://127.0.0.1:8900/game")
    client.login("Bot-" + str(random.randint(0, 999999)))
    client.room_add("BotRoom")
    client.room_join("BotRoom")

    while client.connected:
        time.sleep(10)



