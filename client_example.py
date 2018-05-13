import game_ai_client as aic
import json
import utils.game as game
import utils.room_manager as room_manager
import utils.game_as.chess as chess_as
import random
import time


move_id = -1


def on_room_update(connection, room):
    """
    Handle room-update response
    if current user is a player, find every move from chess state and choose one randomly
    """
    if connection.user.role_id != room_manager.ROLE_SPECTATOR:
        if not connection.user.ready:
            connection.room_command(room_manager.CMD_READY)
            move_id = -1

    can_play = False
    # test if players role is the same as the current turn
    if connection.user.role_id == room_manager.ROLE_WHITE:
        can_play = game.COLOR_WHITE == room.game.turn
    elif connection.user.role_id == room_manager.ROLE_BLACK:
        can_play = game.COLOR_BLACK == room.game.turn

    if room.players_ready and can_play:

        """
        Requests are asynchronous
        that's why the client could work with an old state and send wrong interpretations.
        As prevention the move_count (count) from game will be used.
        The count will work like a timestamp and is unique.
        Comparing these will make it possible to differ between old and new states.
        """

        global move_id
        # only check for moves if the move_id (timestamp) is higher than the old
        # initial value is -1 because the initial count value is 0 (counter fro moves)
        if room.game.state.game_state == game.ChessState.STATE_OK and room.game.count > move_id:
            # generate field from game object (parsed by utils class)
            field = chess_as.get_field(room.game)
            # get every possible move from current field and turn (color)
            moves = chess_as.get_valid_moves(field, room.game.turn)
            if len(moves) > 0:
                move = moves[random.randint(0, len(moves) - 1)][0]
                print("{} Moves -> {}".format(len(moves), move))
                # send move
                connection.game_move(move)
                # set move_id (the timestamp) for the recently submitted move
                move_id = room.game.count
    if room.game.state.game_state != game.ChessState.STATE_OK:
        connection.room_command(room_manager.CMD_RESTART)


def on_room_join(connection, room):
    """
    Handle room-join/room-add event
    set role of current user
    """
    role_black_taken = False
    role_white_taken = False
    # check if any player role is free
    for user in room.users:
        if user.role == room_manager.ROLE_WHITE_STR:
            role_white_taken = True
        if user.role == room_manager.ROLE_BLACK_STR:
            role_black_taken = True
    # send role request
    if not role_black_taken:
        connection.role_change(room_manager.ROLE_BLACK)
    elif not role_white_taken:
        connection.role_change(room_manager.ROLE_WHITE)


if __name__ == "__main__":
    print("API Client 1.0")

    client = aic.GameAIClient()
    client.connect("wss://vg-development.de:8900/game")
    client.login("Bot-" + str(random.randint(0, 999999)))
    client.room_add("BotRoom")
    client.room_join("BotRoom")

    move_done = False

    while client.ws.connected:
        msg = client.receive()
        if msg is None:
            continue
        msg_json = json.loads(msg)
        # get method from json response
        method = msg_json[aic.GameAIClient.METHOD]
        if method == aic.GameAIClient.METHOD_ERROR:
            print("Error {}".format(msg_json["data"]["error"]))

        if method == aic.GameAIClient.METHOD_ROOM_JOIN or method == aic.GameAIClient.METHOD_ROOM_ADD:
            # Convert room json object with the Room wrapper in room_manager.py
            current_room = room_manager.Room(msg_json["data"])
            on_room_join(client, current_room)

        if msg_json[aic.GameAIClient.METHOD] == aic.GameAIClient.METHOD_ROOM_UPDATE:
            current_room = room_manager.Room(msg_json["data"])
            on_room_update(client, current_room)


