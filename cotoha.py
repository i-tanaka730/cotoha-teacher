import requests
import json
from os import environ
from codecs import decode

class CotohaApi:

    DEVELOPER_API_BASE_URL = "https://api.ce-cotoha.com/api/dev/nlp/"
    DEVELOPER_API_SENTIMENT_URL = DEVELOPER_API_BASE_URL + "v1/sentiment"
    ACCESS_TOKEN_PUBLISH_URL = "https://api.ce-cotoha.com/v1/oauth/accesstokens"

    def __init__(self, client_id = "", client_secret = ""):
        self.client_id = environ["CLIENT_ID"] if not client_id else client_id
        self.client_secret = environ["CLIENT_SECRET"] if not client_secret else client_secret

    def get_access_token(self):
        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }

        data = {
            "grantType": "client_credentials",
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }

        response = requests.post(self.ACCESS_TOKEN_PUBLISH_URL, headers=headers, data=json.dumps(data))
        return response.json()["access_token"]

    def sentiment(self, sentence):
        headers = {
            "Authorization": "Bearer " + self.get_access_token(),
            "Content-Type": "application/json;charset=UTF-8",
        }

        data = {
            "sentence": sentence
        }

        response = requests.post(self.DEVELOPER_API_SENTIMENT_URL, headers=headers, data=json.dumps(data))
        return response.json()

if __name__ == "__main__":
    # 以下のパラメータを設定して「python .\cotoha.py」を実行すれば、
    # 当モジュール単体での結果確認が可能
    client_id = ""
    client_secret = ""
    text = "今日は楽しい1日でした。"

    cotoha_api = CotohaApi(client_id, client_secret)
    sentiment_result = cotoha_api.sentiment(text)
    sentiment_formated = json.dumps(sentiment_result, indent=4)
    print (decode(sentiment_formated, 'unicode-escape'))