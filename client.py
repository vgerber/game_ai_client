import game_ai_client
import json
import utils.room_manager


def on_message(message):
    message_json = json.loads(message)
    print("Message: {}".format(json.loads(message)))


def exit_handler():
    print("Closing")


if __name__ == "__main__":
    print("API Client 1.0")
    client = game_ai_client.GameAIClient(on_message)
    client.connect("wss://vg-development.de:8900/game")
    client.login("Hans")
    client.room_all()
    client.room_join("BotRoom", "bot")
    while True:
        pass





