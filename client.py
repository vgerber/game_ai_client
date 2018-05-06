import game_ai_client as aic
import json
import utils.room_manager
import utils.game_as.chess as chess_as


def on_message(msg):
    msg_json = json.loads(msg)
    print(msg_json[aic.GameAIClient.METHOD])

    if msg_json[aic.GameAIClient.METHOD] == aic.GameAIClient.METHOD_ERROR:
        print(msg)

    if msg_json[aic.GameAIClient.METHOD] == aic.GameAIClient.METHOD_ROOM_UPDATE:
        assistant = chess_as.ChessAssistant(msg_json["data"]["game"])
        print(assistant.get_position("a3"))
    #print("Message: {}".format(json.loads(message)))


def exit_handler():
    print("Closing")


if __name__ == "__main__":
    print("API Client 1.0")
    client = aic.GameAIClient(on_message)
    client.connect("ws://localhost:8900/game")
    client.login("Peter")
    client.room_all()
    client.room_add("BotRoom")
    #client.disconnect()
    while True:
        pass





