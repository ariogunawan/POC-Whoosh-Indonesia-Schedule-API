import json

import requests


class BotLine:
    secret_token = ("")
    endpoint_url = "https://api.line.me/v2/bot/message/push"
    destination_id_test = ""  # Chat Bot
    destination_id_real = ""  # Group Keluarga
    auth_bearer = f"Bearer {secret_token}"
    headers = {"Content-Type": "application/json", "Authorization": auth_bearer}

    def __init__(self, test_mode="Y"):
        self.data = None
        self.destination_id = self.set_destination_id(test_mode)

    def set_destination_id(self, test_mode=None) -> str:
        return self.destination_id_real if test_mode == 'N' else self.destination_id_test

    def set_chat_message(self, chat=None) -> object:
        self.data = {"to": self.destination_id,
                     "messages": [{"type": "text", "text": chat}]
                     }
        return self.data

    def send_to_chat(self, chat=None) -> json:
        return json.loads(requests.post(self.endpoint_url, data=json.dumps(self.set_chat_message(chat)), headers=self.headers, verify=False).text)


""" DEBUG
if __name__ == "__main__":
    chat_message = f"\N{Robot Face}: Testing - {datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    bot = BotLine(test_mode="Y")
    response = bot.send_to_chat(chat=chat_message)
    print(f"Response = {json.dumps(response, indent=2)}")
"""

""" COMMON DATA
        self.data = {"to": self.destination_id,
                     "messages": [
                         {"type": "text",
                          "text": f"$ {chat} $",
                          "emojis": [
                              {"index": 0,
                               "productId": "5ac2213e040ab15980c9b447",
                               "emojiId": "001"}
                          ]
                          },
                         {"type": "sticker",
                          "packageId": "6136",
                          "stickerId": "10551377"
                          }
                     ]
                     }
"""
